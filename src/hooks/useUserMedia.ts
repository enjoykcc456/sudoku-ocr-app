import { useState, useEffect } from 'react'

interface MediaTrackConstraints {
  width?: {
    min: number
    ideal: number
    max: number
  }
  height?: {
    min: number
    ideal: number
    max: number
  }
  facingMode?: string
}

export interface MediaStreamConstraints {
  audio?: boolean | MediaTrackConstraints
  video?: boolean | MediaTrackConstraints
}

export const useUserMedia = (constraints: MediaStreamConstraints) => {
  const [mediaStream, setMediaStream] = useState<MediaStream | null>(null)

  useEffect(() => {
    const enableVideoStream = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints)
        console.log(stream)
        setMediaStream(stream)
      } catch (err) {
        console.log(err)
      }
    }

    if (!mediaStream) {
      enableVideoStream()
    } else {
      return function cleanup() {
        mediaStream.getTracks().forEach(track => {
          track.stop()
        })
      }
    }
  }, [mediaStream, constraints])

  return mediaStream
}
