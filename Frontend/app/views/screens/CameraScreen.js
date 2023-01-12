import { Text, View, StyleSheet, TouchableOpacity, Image, Dimensions } from 'react-native';
import { useContext, useEffect, useRef, useState } from 'react';

import { Camera, CameraType } from 'expo-camera';
import { Video } from 'expo-av'
import { manipulateAsync, FlipType, SaveFormat } from 'expo-image-manipulator';
import * as FaceDetector from 'expo-face-detector'

import { AppContext } from '../../contexts/AppContext';

import Colors from '../../config/Colors';

export default function CameraScreen() {
    const [hasCameraPermissions, setHasCameraPermissions] = useState()
    const [photo, setPhoto] = useState()
    const [video, setVideo] = useState()

    const [isRecording, setIsRecording] = useState(false)
    const [type, setType] = useState(CameraType.front)

    const [isFace, setIsFace] = useState(false)
    const [faceRect, setFaceRect] = useState()

    const { AnalyzeImage } = useContext(AppContext)

    const cameraRef = useRef(null)

    const screenWidth = Dimensions.get('window').width
    const screenHeight = Dimensions.get('window').height

    useEffect(() => {
        (async () => {
            const cameraPermission = await Camera.requestCameraPermissionsAsync()
            setHasCameraPermissions(cameraPermission)
        })()
    }, [])

    if (hasCameraPermissions === undefined) {
        return <Text>Requesting Camera Permissions...</Text>
    }else if(hasCameraPermissions === false) {
        return <Text>Requires Permission To Use Camera!</Text>
    }
    
    const SwitchCamera = () => {
        setType(type === CameraType.back ? CameraType.front : CameraType.back)
    }

    const Preprocess = async(newPhoto) => {
        const growthFactor = {
            w: newPhoto.width / screenWidth,
            h: newPhoto.height / screenHeight,
        }

        const processedPhoto = await manipulateAsync(
            newPhoto.localUri || newPhoto.uri,
            [
                { flip: FlipType.Horizontal },
                { crop: {
                    originX: Math.round(faceRect.x * growthFactor.w),
                    originY: Math.round(faceRect.y * growthFactor.h),
                    width: Math.round(faceRect.width * growthFactor.w),
                    height: Math.round(faceRect.width * growthFactor.w),
                }},
                {resize: {
                    width: 400
                }}
            ],
            { compress: 0.3, format: SaveFormat.JPEG , base64: true }
        );
        
        return processedPhoto
    }

    const CapturePicture = async() => {
        const options = {
            quality: 1,
            base64: true,
            exif: false,
        }

        let newPhoto = await cameraRef.current.takePictureAsync(options)
        let newnewPhoto = await Preprocess(newPhoto)

        setPhoto(newnewPhoto)
        setPhoto(photo => {
            AnalyzeImage(photo.base64, photo.width, photo.height)
            return photo
        })
    }

    const CaptureVideo = async() => {
        const options = {
            quality: '720p',
            maxDuration: 2,
            mute: true,
            framerate: 5
        }

        cameraRef.current.recordAsync(options).then((vid) => {
            setVideo(vid)
            setIsRecording(false)
        })
    }

    const EndVideoCapture = () => {
        cameraRef.current.stopRecording()
        setIsRecording(false)
    }

    const handleFacesDetected = ({ faces }) => {
        if(faces.length === 0) { setIsFace(false); return; }

        if(isFace === false) setIsFace(true)

        const data = faces[0].bounds

        const cropDimensions = {
            x: data.origin.x,
            y: data.origin.y,
            width: data.size.height,
            height: data.size.height
        }

        setFaceRect(cropDimensions)
    }

    if(video) {
        return (
            <View style={styles.container}>
                <Video
                    style={styles.preview}
                    source={{uri: video.uri}}
                    useNativeControls
                    resizeMode='contain'
                    isLooping
                />
            </View>
        )
    }
    let isCapturing = false
    let interval = undefined

    const ToggleCapture = () => {
        if(isCapturing == true) {
            isCapturing = false
            clearInterval(interval)
            return
        }

        isCapturing = true
        interval = setInterval(CapturePicture, 2000)
    }

    return (
        <Camera style={styles.container} type={type} ref={cameraRef}
            onFacesDetected={handleFacesDetected}
            faceDetectorSettings={{
                mode: FaceDetector.FaceDetectorMode.fast,
                detectLandmarks: FaceDetector.FaceDetectorLandmarks.none,
                runClassifications: FaceDetector.FaceDetectorClassifications.none,
                minDetectionInterval: 100,
                tracking: true,
            }}>
            <TouchableOpacity style={styles.backArrow} onPress={() => {navigation.navigate('Home')}}>
                <Image source={require('../../assets/back-icon.png')} style={styles.fillImage} />
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.switchButton} onPress={ToggleCapture}>
                <Image source={require('../../assets/switch-icon.png')} style={styles.fillImage} />
            </TouchableOpacity>

            {isFace && faceRect !== undefined ? <View style={{
                position: 'absolute',
                left: faceRect.x,
                top: faceRect.y,
                width: faceRect.width,
                height: faceRect.height,
                borderWidth: 1,
                borderColor: Colors.Green
            }} /> : ''}
            
            <View style={styles.interactionBar}>
                
            </View>
        </Camera>
    )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    interactionBar: {
        position: 'absolute',
        bottom: 15,
        width: '100%',
        height: 70,
        justifyContent: 'center',
        alignItems: 'center'
    },
    captureButton: {
        backgroundColor: Colors.White,
        width: 60,
        height: 60, 
        borderRadius: 30
    },
    captureButtonHighlight: {
        width: 70,
        height: 70,
        borderRadius: 50,
        borderWidth: 3,
        borderColor: Colors.White,

        justifyContent: 'center',
        alignItems: 'center'
    },
    backArrow: {
        position: 'absolute',
        left: 10,
        top: 20,

        width: 30,
        height: 30
    },
    switchButton: {
        position: 'absolute',
        right: 10,
        top: 20,

        width: 30,
        height: 30
    },
    fillImage:{
        width: '100%',
        height: '100%'
    },
    capture: {
        position: 'absolute',
        left: 0,
        right: 0,
        top: 0,
        bottom: 0,
        zIndex: 10,
        backgroundColor: Colors.White
    },
    icon: {
        width: 60,
        height: 60,
        bottom: 10,
        position: 'absolute',
        overflow: 'hidden',
        borderRadius: 50
    },
    accept: {
        left: 10,
        backgroundColor: Colors.White
    },
    delete: {
        right: 10,
        backgroundColor: Colors.White
    },
    preview: {
      alignSelf: 'stretch',
      flex: 1
    }
})