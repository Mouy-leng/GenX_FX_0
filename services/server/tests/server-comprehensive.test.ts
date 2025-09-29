import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import request from 'supertest';
import WebSocket, { WebSocketServer } from 'ws';
import express from 'express';
import { createServer, Server as HttpServer } from 'http';
import cors from 'cors';

// Mock dependencies
vi.mock('../routes.ts', () => ({
  registerRoutes: vi.fn((app) => {
    app.get('/api/test', (req, res) => res.json({ message: 'test endpoint' }));
    app.post('/api/data', (req, res) => res.json({ received: req.body }));
    app.get('/api/error', (req, res) => { throw new Error('Test error'); });
  })
}));

vi.mock('../vite.ts', () => ({
  setupVite: vi.fn(),
  serveStatic: vi.fn()
}));

describe('GenX FX Server Comprehensive Tests', () => {
  let app: express.Application;
  let server: HttpServer;
  let wss: WebSocketServer;
  let baseURL: string;
  const activeSockets = new Set<WebSocket>();

  beforeAll(async () => {
    app = express();
    
    app.use(cors({ origin: true, credentials: true }));
    app.use(express.json({ limit: '10mb' }));
    app.use(express.urlencoded({ extended: true }));

    app.get('/health', (req, res) => {
      res.json({ 
        status: 'OK', 
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV || 'development'
      });
    });

    const { registerRoutes } = await import('../routes.ts');
    registerRoutes(app);

    // Specific error handler for body-parser issues
    app.use((err: any, req, res, next) => {
      if (err instanceof SyntaxError && 'body' in err) {
        return res.status(400).json({ error: 'Malformed JSON' });
      }
      if (err.type === 'entity.too.large') {
        return res.status(413).json({ error: 'Payload Too Large' });
      }
      next(err);
    });

    // Generic error handler
    app.use((err: any, req, res, next) => {
      res.status(500).json({
        error: 'Internal server error',
        message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
      });
    });

    // Correct 404 handler
    app.use((req, res) => {
      res.status(404).json({
        error: 'Not found',
        path: req.originalUrl
      });
    });

    server = createServer(app);

    // WebSocket server setup
    wss = new WebSocketServer({ server });
    wss.on('connection', (ws) => {
      activeSockets.add(ws);
      ws.on('close', () => activeSockets.delete(ws));

      ws.send(JSON.stringify({
        type: 'welcome',
        message: 'Connected to GenZ Trading Bot Pro',
        timestamp: new Date().toISOString()
      }));

      ws.on('message', (message) => {
        try {
          const parsed = JSON.parse(message.toString());
          ws.send(JSON.stringify({ type: 'echo', data: parsed, timestamp: new Date().toISOString() }));
        } catch (e) {
          ws.send(JSON.stringify({ type: 'error', message: 'Invalid JSON format' }));
        }
      });
    });

    const port = 5001; // Use a fixed port for predictability in tests
    await new Promise<void>(resolve => server.listen(port, resolve));
    baseURL = `http://localhost:${port}`;
  });

  // Graceful shutdown
  afterAll(async () => {
    await new Promise<void>(resolve => {
      for (const socket of activeSockets) {
        socket.terminate();
      }
      wss.close(() => {
        server.close(() => resolve());
      });
    });
  });

  describe('HTTP Server Tests', () => {
    it('should return health check with correct format', async () => {
      const response = await request(app).get('/health');
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('status', 'OK');
      expect(response.body).toHaveProperty('timestamp');
      expect(response.body).toHaveProperty('environment');
      expect(new Date(response.body.timestamp)).toBeInstanceOf(Date);
    });

    it('should handle CORS correctly', async () => {
      const response = await request(app).get('/health').set('Origin', 'http://localhost:3000');
      expect(response.headers['access-control-allow-origin']).toBe('http://localhost:3000');
      expect(response.headers['access-control-allow-credentials']).toBe('true');
    });

    it('should parse JSON correctly', async () => {
      const testData = { test: 'data', number: 123, nested: { value: true } };
      const response = await request(app).post('/api/data').send(testData);
      expect(response.status).toBe(200);
      expect(response.body.received).toEqual(testData);
    });

    it('should handle large JSON payloads (under 10MB limit)', async () => {
      const largeData = {
        data: 'x'.repeat(1024 * 1024),
        array: new Array(1000).fill({ test: 'data' })
      };
      const response = await request(app).post('/api/data').send(largeData);
      expect(response.status).toBe(200);
      expect(response.body.received.data).toBe(largeData.data);
    });

    it('should reject payloads exceeding 10MB limit', async () => {
      const oversizedData = { data: 'x'.repeat(11 * 1024 * 1024) };
      const response = await request(app).post('/api/data').send(oversizedData);
      expect(response.status).toBe(413);
    });

    it('should handle malformed JSON gracefully', async () => {
      const response = await request(app).post('/api/data').set('Content-Type', 'application/json').send('{ invalid json }');
      expect(response.status).toBe(400);
    });

    it('should handle server errors with proper error response', async () => {
      const response = await request(app).get('/api/error');
      expect(response.status).toBe(500);
    });

    it('should return 404 for unknown routes', async () => {
      const response = await request(app).get('/non-existent-route');
      expect(response.status).toBe(404);
    });
  });

  describe('Edge Cases', () => {
    it('should handle empty request body', async () => {
      const response = await request(app).post('/api/data').send({});
      expect(response.status).toBe(200);
      expect(response.body.received).toEqual({});
    });

    it('should handle null values in JSON', async () => {
      const testData = { nullValue: null, emptyString: '', zero: 0, falseValue: false };
      const response = await request(app).post('/api/data').send(testData);
      expect(response.status).toBe(200);
      expect(response.body.received).toEqual(testData);
    });

    it('should handle special characters and unicode', async () => {
      const testData = { emoji: '🚀', unicode: 'café' };
      const response = await request(app).post('/api/data').send(testData);
      expect(response.status).toBe(200);
      expect(response.body.received).toEqual(testData);
    });

    it('should handle arrays with mixed types', async () => {
      const testData = { mixedArray: [1, 'string', null, { a: 1 }] };
      const response = await request(app).post('/api/data').send(testData);
      expect(response.status).toBe(200);
      expect(response.body.received).toEqual(testData);
    });

    it('should handle deeply nested objects', async () => {
      const testData = { level1: { level2: { level3: { level4: { level5: 'found' } } } } };
      const response = await request(app).post('/api/data').send(testData);
      expect(response.status).toBe(200);
      expect(response.body.received.level1.level2.level3.level4.level5).toBe('found');
    });
  });

  describe('WebSocket Tests', () => {
    it('should establish WebSocket connection and send welcome message', async () => {
      const ws = new WebSocket(baseURL.replace('http', 'ws'));
      await new Promise<void>((resolve, reject) => {
        ws.on('message', (data) => {
          const message = JSON.parse(data.toString());
          if (message.type === 'welcome') {
            expect(message.message).toBe('Connected to GenZ Trading Bot Pro');
            ws.close();
            resolve();
          }
        });
        ws.on('error', reject);
      });
    });

    it('should echo back valid JSON messages', async () => {
      const ws = new WebSocket(baseURL.replace('http', 'ws'));
      const testMessage = { action: 'test', data: { value: 123 } };
      await new Promise<void>((resolve, reject) => {
        ws.on('open', () => {
          ws.send(JSON.stringify(testMessage));
        });
        ws.on('message', (data) => {
          const message = JSON.parse(data.toString());
          if (message.type === 'echo') {
            expect(message.data).toEqual(testMessage);
            ws.close();
            resolve();
          }
        });
        ws.on('error', reject);
      });
    });

    it('should handle invalid JSON messages gracefully', async () => {
      const ws = new WebSocket(baseURL.replace('http', 'ws'));
      await new Promise<void>((resolve, reject) => {
        ws.on('open', () => {
          ws.send('{ invalid json }');
        });
        ws.on('message', (data) => {
          const message = JSON.parse(data.toString());
          if (message.type === 'error') {
            expect(message.message).toBe('Invalid JSON format');
            ws.close();
            resolve();
          }
        });
        ws.on('error', reject);
      });
    });
  });
});