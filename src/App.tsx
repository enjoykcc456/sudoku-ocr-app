import React, { useState } from 'react'
import './styles/index.css'
import { Camera } from './components/camera/camera.component'
import { Button } from '@material-ui/core'

function App() {
  const [isCameraOpen, setIsCameraOpen] = useState<boolean>(false)
  const [cardImage, setCardImage] = useState()

  return (
    <div className="App">
      <header className="App-header">
        {isCameraOpen && <Camera />}
        <Button onClick={() => setIsCameraOpen(true)}>Open Camera</Button>
        <Button
          onClick={() => {
            setIsCameraOpen(false)
            setCardImage(undefined)
          }}
        >
          Close Camera
        </Button>
      </header>
    </div>
  )
}

export default App
