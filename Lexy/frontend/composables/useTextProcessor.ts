export function useTextProcessor() {
  const processText = (content: string, highlight: boolean = true) => {
    const tempDiv = document.createElement('div')
    tempDiv.innerHTML = content

    const processNode = (node: Node) => {
      if (node.nodeType === 3) { // Text node
        const words = node.textContent!.split(/(\s+)/)
        const span = document.createElement('span')
        span.innerHTML = words.map(word => {
          if (word.trim()) {
            return `<span data-word="${word}" class="${highlight ? 'word-highlight hover:bg-purple-300/50 hover:text-black dark:hover:bg-violet-900/50 dark:hover:text-white hover:scale-110' : ''}">${word}</span>`
          }
          return word
        }).join('')
        node.parentNode!.replaceChild(span, node)
      } else if (node.nodeType === 1) { // Element node
        Array.from(node.childNodes).forEach(processNode)
      }
    }

    processNode(tempDiv)
    return tempDiv.innerHTML
  }

  return {
    processText
  }
}
