/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Base URL for backend API calls. Falls back to "/api" when unset. */
  readonly VITE_API_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
