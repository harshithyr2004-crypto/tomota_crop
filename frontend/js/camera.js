// -*- coding: utf-8 -*-
/**
 * Live Camera Capture and Viewport Manager
 */

class CameraManager {
    constructor() {
        this.video = document.getElementById('cameraVideo');
        this.canvas = document.getElementById('cameraCanvas');
        this.viewportContainer = document.getElementById('cameraViewportContainer');
        this.dropzone = document.getElementById('dropzone');
        this.stream = null;
        this.facingMode = 'environment'; // Default to back camera on mobile
    }

    async openCamera() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert('Camera access is not supported by your browser or requires HTTPS / localhost.');
            return false;
        }

        try {
            if (this.stream) {
                this.closeCamera();
            }

            const constraints = {
                video: {
                    facingMode: this.facingMode,
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                },
                audio: false
            };

            this.stream = await navigator.mediaDevices.getUserMedia(constraints);
            this.video.srcObject = this.stream;
            
            this.dropzone.classList.add('hidden');
            this.viewportContainer.classList.remove('hidden');
            return true;
        } catch (error) {
            console.error('Camera open error:', error);
            if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
                alert('⚠️ Camera permission was denied. Please allow camera permissions in your browser settings.');
            } else {
                alert(`⚠️ Could not access camera: ${error.message}`);
            }
            return false;
        }
    }

    closeCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        this.viewportContainer.classList.add('hidden');
        this.dropzone.classList.remove('hidden');
    }

    async switchCamera() {
        this.facingMode = (this.facingMode === 'environment') ? 'user' : 'environment';
        await this.openCamera();
    }

    captureSnapshot() {
        if (!this.video || !this.stream) return null;

        const w = this.video.videoWidth || 640;
        const h = this.video.videoHeight || 480;

        this.canvas.width = w;
        this.canvas.height = h;
        const ctx = this.canvas.getContext('2d');
        ctx.drawImage(this.video, 0, 0, w, h);

        return new Promise((resolve) => {
            this.canvas.toBlob((blob) => {
                const file = new File([blob], `camera_snap_${Date.now()}.jpg`, { type: 'image/jpeg' });
                this.closeCamera();
                resolve(file);
            }, 'image/jpeg', 0.95);
        });
    }
}

window.cameraManager = new CameraManager();
