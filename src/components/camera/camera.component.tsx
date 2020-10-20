import React, { useState, useRef, useCallback, useEffect } from 'react'
import { useUserMedia, MediaStreamConstraints } from '../../hooks/useUserMedia'

interface ContainerDimension {
  width: number
  height: number
}

const CONSTRAINTS: MediaStreamConstraints = {
  audio: false,
  video: true,
}

export const Camera = () => {
  const videoRef = useRef<any | null>(null)
  const canvasRef = useRef<any | null>(null)

  const [container, setContainer] = useState<ContainerDimension>({
    width: 0,
    height: 0,
  })
  const [isVideoPlaying, setIsVideoPlaying] = useState<boolean>(false)
  const [isCanvasEmpty, setIsCanvasEmpty] = useState<boolean>(true)
  const [isFlashing, setIsFlashing] = useState<boolean>(false)

  const mediaStream = useUserMedia(CONSTRAINTS)

  useEffect(() => {
    if (mediaStream && videoRef.current && !videoRef.current.srcObject) {
      console.log('set media stream to video')
      videoRef.current.srcObject = mediaStream
    }
  }, [mediaStream])

  console.log('media stream', mediaStream)
  console.log('video ref', videoRef.current)

  if (!mediaStream) {
    return null
  }

  const handleCanPlay = () => {
    console.log('set video playing and play video')
    setIsVideoPlaying(true)
    videoRef.current.play()
  }

  return (
    <div>
      <video
        ref={videoRef}
        hidden={false}
        onCanPlay={handleCanPlay}
        autoPlay
        playsInline
        muted
      />
    </div>
  )
}
