import globals from "globals";
import tseslint from "typescript-eslint";
import pluginReactConfig from "eslint-plugin-react/configs/recommended.js";

export default [
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
  },
  {
    files: ["**/*.{js,jsx,mjs,cjs,ts,tsx}"],
    ...pluginReactConfig,
    settings: {
      react: {
        version: "detect", // Automatically detect the React version
      },
    },
    rules: {
      ...pluginReactConfig.rules,
      "react/react-in-jsx-scope": "off", // Disable the rule for new JSX transform
      "react/jsx-uses-react": "off", // Disable the rule for new JSX transform
    },
  },
  ...tseslint.configs.recommended,
];