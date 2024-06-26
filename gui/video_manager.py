import cv2, math
from PIL import ImageTk, Image
from tkinter import simpledialog

class VideoProcessor:
    def __init__(self, video_path):
        self.vid_path = video_path
        
        self.video = cv2.VideoCapture(video_path)
        self.total_frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        self.current_frame_count = 0
        if not self.video.isOpened():
            raise ValueError("Error opening video file")
        self.roi_1 = None
        self.roi_2 = None
        self.scale = None

    def get_vid_path(self):
        return self.vid_path
    
    def get_current_frame_count(self):
        return self.current_frame_count
    
    def get_total_frame_count(self):
        return self.total_frame_count
    
    def get_current_image(self):
        return self.current_image
    
    def get_next_frame(self, num):
        new_frame = self.current_frame_count + num
        if new_frame < 0:
            new_frame = 0
        elif new_frame > self.total_frame_count:
            new_frame = self.total_frame_count

        cap = cv2.VideoCapture(self.vid_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
        res, frame = cap.read()
        if res:
            self.current_image = frame
            #keep reference to avoid garbage collection
            self.frame_image = self.render_image(frame)
            self.current_frame_count = new_frame
            return self.frame_image

    def render_image(self, image):
        image = cv2.resize(image, (500,300), interpolation = cv2.INTER_LINEAR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        return ImageTk.PhotoImage(image=image) 
    
    def select_roi(self, roi_num):
        img = self.current_image
        x, y, w, h = cv2.selectROI(img)
        cv2.destroyAllWindows()
        rect = (x, y, w, h)
        if roi_num == 1:
            self.roi_1 = rect
        elif roi_num == 2:
            self.roi_2 = rect
        return rect

    def setup_draw(self):
        self.points = []
        self.scale_img = self.current_image.copy()
        cv2.namedWindow("scale_window")
        cv2.setMouseCallback("scale_window", self.draw_event)
        cv2.imshow("scale_window", self.scale_img)
        cv2.waitKey(0)

    def draw_event(self, event, x, y, flags, userdata):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x, y))
            if len(self.points) == 1:
                cv2.circle(self.scale_img, self.points[0], 5, (0, 0, 255), -1)
                cv2.imshow("scale_window", self.scale_img)
            elif len(self.points) == 2:
                cv2.circle(self.scale_img, self.points[1], 5, (0, 0, 255), -1)
                cv2.line(self.scale_img, self.points[0], self.points[1], (0, 255, 0), 2)
                cv2.imshow("scale_window", self.scale_img)
                pixel_length = math.sqrt((self.points[1][0] - self.points[0][0]) ** 2 + (self.points[1][1] - self.points[0][1]) ** 2)
                cv2.setMouseCallback("scale_window", lambda *args: None)  # Disable further callbacks

                real_world_length = simpledialog.askfloat("Input", "Enter the real-world length (meters) of the line:")
                if real_world_length is not None:
                    self.scale = real_world_length / pixel_length
                    cv2.destroyAllWindows()

    def check_roi_exists(self):
        return self.roi_1 is not None and self.roi_2 is not None
        
    def check_scale_exists(self):
        return self.scale is not None
    
    def get_scale(self):
        return self.scale
    