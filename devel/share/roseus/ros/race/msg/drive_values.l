;; Auto-generated. Do not edit!


(when (boundp 'race::drive_values)
  (if (not (find-package "RACE"))
    (make-package "RACE"))
  (shadow 'drive_values (find-package "RACE")))
(unless (find-package "RACE::DRIVE_VALUES")
  (make-package "RACE::DRIVE_VALUES"))

(in-package "ROS")
;;//! \htmlinclude drive_values.msg.html


(defclass race::drive_values
  :super ros::object
  :slots (_pid_vel _pid_error _z _a _b _dist_CD _dist_AB _alpha _realvel _theta1 _theta2 ))

(defmethod race::drive_values
  (:init
   (&key
    ((:pid_vel __pid_vel) 0.0)
    ((:pid_error __pid_error) 0.0)
    ((:z __z) 0.0)
    ((:a __a) 0.0)
    ((:b __b) 0.0)
    ((:dist_CD __dist_CD) 0.0)
    ((:dist_AB __dist_AB) 0.0)
    ((:alpha __alpha) 0.0)
    ((:realvel __realvel) 0.0)
    ((:theta1 __theta1) 0.0)
    ((:theta2 __theta2) 0.0)
    )
   (send-super :init)
   (setq _pid_vel (float __pid_vel))
   (setq _pid_error (float __pid_error))
   (setq _z (float __z))
   (setq _a (float __a))
   (setq _b (float __b))
   (setq _dist_CD (float __dist_CD))
   (setq _dist_AB (float __dist_AB))
   (setq _alpha (float __alpha))
   (setq _realvel (float __realvel))
   (setq _theta1 (float __theta1))
   (setq _theta2 (float __theta2))
   self)
  (:pid_vel
   (&optional __pid_vel)
   (if __pid_vel (setq _pid_vel __pid_vel)) _pid_vel)
  (:pid_error
   (&optional __pid_error)
   (if __pid_error (setq _pid_error __pid_error)) _pid_error)
  (:z
   (&optional __z)
   (if __z (setq _z __z)) _z)
  (:a
   (&optional __a)
   (if __a (setq _a __a)) _a)
  (:b
   (&optional __b)
   (if __b (setq _b __b)) _b)
  (:dist_CD
   (&optional __dist_CD)
   (if __dist_CD (setq _dist_CD __dist_CD)) _dist_CD)
  (:dist_AB
   (&optional __dist_AB)
   (if __dist_AB (setq _dist_AB __dist_AB)) _dist_AB)
  (:alpha
   (&optional __alpha)
   (if __alpha (setq _alpha __alpha)) _alpha)
  (:realvel
   (&optional __realvel)
   (if __realvel (setq _realvel __realvel)) _realvel)
  (:theta1
   (&optional __theta1)
   (if __theta1 (setq _theta1 __theta1)) _theta1)
  (:theta2
   (&optional __theta2)
   (if __theta2 (setq _theta2 __theta2)) _theta2)
  (:serialization-length
   ()
   (+
    ;; float32 _pid_vel
    4
    ;; float32 _pid_error
    4
    ;; float32 _z
    4
    ;; float32 _a
    4
    ;; float32 _b
    4
    ;; float32 _dist_CD
    4
    ;; float32 _dist_AB
    4
    ;; float32 _alpha
    4
    ;; float32 _realvel
    4
    ;; float32 _theta1
    4
    ;; float32 _theta2
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _pid_vel
       (sys::poke _pid_vel (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _pid_error
       (sys::poke _pid_error (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _z
       (sys::poke _z (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _a
       (sys::poke _a (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _b
       (sys::poke _b (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _dist_CD
       (sys::poke _dist_CD (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _dist_AB
       (sys::poke _dist_AB (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _alpha
       (sys::poke _alpha (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _realvel
       (sys::poke _realvel (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _theta1
       (sys::poke _theta1 (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _theta2
       (sys::poke _theta2 (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _pid_vel
     (setq _pid_vel (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _pid_error
     (setq _pid_error (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _z
     (setq _z (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _a
     (setq _a (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _b
     (setq _b (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _dist_CD
     (setq _dist_CD (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _dist_AB
     (setq _dist_AB (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _alpha
     (setq _alpha (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _realvel
     (setq _realvel (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _theta1
     (setq _theta1 (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _theta2
     (setq _theta2 (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get race::drive_values :md5sum-) "b3201a025913db3e51dc81dc52587e75")
(setf (get race::drive_values :datatype-) "race/drive_values")
(setf (get race::drive_values :definition-)
      "float32 pid_vel
float32 pid_error
float32 z
float32 a
float32 b
float32 dist_CD
float32 dist_AB
float32 alpha
float32 realvel
float32 theta1
float32 theta2

")



(provide :race/drive_values "b3201a025913db3e51dc81dc52587e75")


