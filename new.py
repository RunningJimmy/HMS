from widget_base.camera import *

if __name__ == "__main__":
    import sys
    import cgitb
    sys.excepthook = cgitb.Hook(1, None, 5, sys.stderr, 'text')
    app = QApplication(sys.argv)
    ui = CameraWidget()
    # ui.on_camera_open()
    ui.show()
    sys.exit(app.exec_())