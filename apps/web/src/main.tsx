/**
 * Ponto de entrada da aplicação React.
 *
 * Estado: PLACEHOLDER funcional (renderiza ChatPage).
 * Adicionar roteamento (react-router-dom) quando houver mais de uma página.
 */

import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { ChatPage } from "./pages/ChatPage"

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ChatPage />
  </StrictMode>
)
