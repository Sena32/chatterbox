import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"

import { StreamingMessageBubble } from "./StreamingMessageBubble"

describe("StreamingMessageBubble", () => {
  it("exibe conteúdo parcial e indicador de streaming", () => {
    render(<StreamingMessageBubble content="Digitando" isStreaming={true} />)

    expect(screen.getByTestId("streaming-bubble")).toHaveTextContent("Digitando")
    expect(screen.getByText("▍")).toBeInTheDocument()
  })

  it("não renderiza quando não há conteúdo e não está streaming", () => {
    const { container } = render(
      <StreamingMessageBubble content="" isStreaming={false} />,
    )
    expect(container).toBeEmptyDOMElement()
  })
})
