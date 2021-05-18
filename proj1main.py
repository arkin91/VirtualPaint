from proj1 import NewWebcam

# from cam import webcamDisplay

print("type q to exit the feed")
# flag = True
wb = NewWebcam()
# while(flag):
wb.webcamdisplay()  # uses cv2.imshow() for displaying frame by frame webcam feed.
                    # also detects orange hues in frame
