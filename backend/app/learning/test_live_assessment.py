import cv2
import time

from app.learning.live_practice import LivePractice



def main():

    print("\nStarting Live Assessment Test\n")


    practice = LivePractice("A")


    print(
        practice.start_practice()
    )


    cap = cv2.VideoCapture(0)


    if not cap.isOpened():

        print("Camera not detected")
        return



    start = time.time()



    while True:


        ret, frame = cap.read()


        if not ret:
            break



        result = practice.process_frame(
            frame
        )


        print(result)



        cv2.imshow(
            "SignSync Assessment",
            frame
        )



        key = cv2.waitKey(1)


        if key == ord('q'):

            break



    cap.release()

    cv2.destroyAllWindows()



    print("\n====================")
    print("FINAL ASSESSMENT")
    print("====================")


    print(
        practice.get_assessment_score()
    )



    print("\nSUMMARY")

    print(
        practice.get_summary()
    )




if __name__ == "__main__":

    main()