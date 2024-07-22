import cv2, math
from PIL import ImageTk, Image
from tkinter import simpledialog

class VideoManager:
    def __init__(self, parent_size):
        self.parent_width = parent_size[0]
        self.parent_height = parent_size[1]

        self.vid_path = None
        self.output_path = None
        self.roi_1 = None
        self.roi_2 = None
        self.scale = None
        self.skip = 1
        self.threshold = None
        self.frame_duration = None
        self.region = None
        self.meter_per_pixel = None

        self.csv_path = None

    def set_video(self, path):
        self.vid_path = path
        self.video = cv2.VideoCapture(path)
        self.total_frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        self.current_frame_count = 0
        if not self.video.isOpened():
            raise ValueError("Error opening video file")

    def get_vid_path(self):
        return self.vid_path
    
    def set_output_path(self, path):
        self.output_path = path
    
    def get_output_path(self):
        return self.output_path
    
    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_threshold(self):
        return self.threshold

    def set_skip(self, num):
        self.skip = num
    
    def get_skip(self):
        return self.skip

    def set_scale(self, num): #TODO: GET RID OF THIS 
        self.scale = num

    def get_scale(self):
        return self.scale
    
    def get_current_frame_count(self):
        return self.current_frame_count
    
    def get_total_frame_count(self):
        return self.total_frame_count
    
    def get_current_image(self):
        return self.current_image
    
    def set_region(self, region):
        self.region = region

    def get_region(self):
        return self.region
    
    def set_frame_duration(self, duration):
        self.frame_duration = duration

    def get_frame_duration(self):
        return self.frame_duration
    
    def set_csv_path(self, path):
        self.csv_path = path

    def get_csv_path(self):
        return self.csv_path
    
    def get_roi(self, num):
        if num == 1:
            return self.roi_image1, self.roi_1
        elif num == 2:
            return self.roi_image2, self.roi_2
    
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
            self.frame_image = self.render_image(frame, 1.5)
            self.current_frame_count = new_frame
            return self.frame_image

    def render_image(self, image, ratio):
        height, width, channels = image.shape
        max_height = int(self.parent_height / ratio)
        max_width = int(self.parent_width / ratio)
        aspect_ratio = width / height
        if height > max_height or width > max_width:
            if max_width / aspect_ratio <= max_height:
                render_size = (max_width, int(max_width / aspect_ratio))
            else:
                render_size = (int(max_height * aspect_ratio), max_height)
        else:
            render_size = (width, height)

        image = cv2.resize(image, render_size, interpolation = cv2.INTER_LINEAR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        return ImageTk.PhotoImage(image=image) 
    
    def select_roi(self, roi_num):
        x, y, w, h = cv2.selectROI(self.current_image)
        cv2.destroyAllWindows()
        rect = (x, y, w, h)
        top_left=(x, x + w)
        bottom_right = (y, y + h)
        if roi_num == 1:
            self.roi_image1 = self.current_image
            self.roi_1 = (top_left, bottom_right)
        elif roi_num == 2:
            self.roi_image2 = self.current_image
            self.roi_2 = (top_left, bottom_right)
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

                real_world_length = simpledialog.askfloat("Input", 
                                                          "Enter the real-world length (meters) of the line:")
                if real_world_length is not None:
                    self.scale = real_world_length / pixel_length
                    cv2.destroyAllWindows()

    def check_roi_exists(self):
        return self.roi_1 is not None and self.roi_2 is not None
        
    def check_scale_exists(self):
        return self.scale is not None