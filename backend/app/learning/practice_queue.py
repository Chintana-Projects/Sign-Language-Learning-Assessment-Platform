from datetime import datetime


class PracticeQueue:

    """
    Adaptive Practice Queue

    Responsible for:
    - Storing personalized alphabet recommendations
    - Maintaining learning order
    - Providing next practice alphabet
    - Removing completed alphabets
    """


    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):

        # Stores queue per student

        self.queues = {}



    # =====================================================
    # GET STUDENT QUEUE
    # =====================================================

    def get_queue(
        self,
        student_id
    ):

        student_id = str(student_id)


        if student_id not in self.queues:

            self.queues[student_id] = []


        return self.queues[student_id]



    # =====================================================
    # UPDATE QUEUE
    # Called after RecommendationEngine
    # =====================================================

    def update_queue(
        self,
        student_id,
        recommendations
    ):

        student_id = str(student_id)


        if not recommendations:

            return self.get_queue(
                student_id
            )


        queue = []


        for item in recommendations:


            alphabet = item.get(
                "alphabet"
            )


            if not alphabet:
                continue



            queue.append({

                "alphabet":
                    alphabet.upper(),


                "reason":
                    item.get(
                        "reason",
                        "Practice required."
                    ),


                "priority":
                    item.get(
                        "priority",
                        "MEDIUM"
                    ),


                "added_at":
                    datetime.now().isoformat()

            })



        # Replace old queue
        # with latest adaptive recommendation

        self.queues[
            student_id
        ] = queue



        print(
            "\n========== PRACTICE QUEUE UPDATED =========="
        )

        print(
            "STUDENT:",
            student_id
        )

        print(
            "QUEUE:",
            queue
        )


        return queue



    # =====================================================
    # GET NEXT PRACTICE
    # =====================================================

    def get_next_practice(
        self,
        student_id
    ):

        queue = self.get_queue(
            student_id
        )


        if not queue:

            return None



        return queue[0]



    # =====================================================
    # GET NEXT ALPHABET ONLY
    # =====================================================

    def get_next_letter(
        self,
        student_id
    ):

        next_item = self.get_next_practice(
            student_id
        )


        if next_item:

            return next_item.get(
                "alphabet"
            )


        return None



    # =====================================================
    # COMPLETE LETTER
    # Remove practiced alphabet
    # =====================================================

    def complete_letter(
        self,
        student_id,
        alphabet
    ):

        student_id = str(
            student_id
        )


        if student_id not in self.queues:

            return []



        alphabet = str(
            alphabet
        ).upper()



        updated_queue = []


        for item in self.queues[student_id]:


            if item.get(
                "alphabet"
            ) != alphabet:


                updated_queue.append(
                    item
                )



        self.queues[
            student_id
        ] = updated_queue



        print(
            "REMOVED FROM QUEUE:",
            alphabet
        )


        return updated_queue



    # =====================================================
    # PEEK QUEUE
    # =====================================================

    def peek_queue(
        self,
        student_id
    ):

        return self.get_queue(
            student_id
        )



    # =====================================================
    # CLEAR QUEUE
    # =====================================================

    def clear_queue(
        self,
        student_id
    ):

        student_id = str(
            student_id
        )


        self.queues[
            student_id
        ] = []


        return []



    # =====================================================
    # REMOVE STUDENT QUEUE
    # =====================================================

    def delete_student_queue(
        self,
        student_id
    ):

        student_id = str(
            student_id
        )


        if student_id in self.queues:

            del self.queues[
                student_id
            ]

            return True


        return False



    # =====================================================
    # GET ALL QUEUES
    # =====================================================

    def get_all_queues(
        self
    ):

        return self.queues