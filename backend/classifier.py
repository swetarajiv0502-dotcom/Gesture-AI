class GestureClassifier:
    def __init__(self):
        pass

    def classify(self, hand_landmarks):
        """
        Classifies hand gesture based on 21 MediaPipe landmarks.
        Returns gesture name string.
        """
        lm = hand_landmarks.landmark

        # Fingertip indices: Thumb=4, Index=8, Middle=12, Ring=16, Pinky=20
        # PIP (middle joint) indices: Index=6, Middle=10, Ring=14, Pinky=18
        # MCP (knuckle) indices: Thumb=2, Index=5, Middle=9, Ring=13, Pinky=17

        # --- Detect which fingers are extended ---
        # For index–pinky: tip.y < pip.y means finger is up (y=0 is top of image)
        index_up  = lm[8].y  < lm[6].y
        middle_up = lm[12].y < lm[10].y
        ring_up   = lm[16].y < lm[14].y
        pinky_up  = lm[20].y < lm[18].y

        # Thumb: compare x of tip vs mcp2 (flipped image)
        thumb_up = lm[4].x < lm[2].x  # on flipped feed, left is smaller x

        four_fingers = index_up and middle_up and ring_up and pinky_up

        # --- Pinch (Thumb tip close to Index tip) ---
        pinch_dist = ((lm[4].x - lm[8].x)**2 + (lm[4].y - lm[8].y)**2) ** 0.5
        if pinch_dist < 0.05:
            return "Pinch"

        # --- Open Palm (all 4 fingers up) ---
        if four_fingers:
            return "Open Palm"

        # --- Closed Fist (no fingers up) ---
        if not index_up and not middle_up and not ring_up and not pinky_up:
            return "Closed Fist"

        # --- Pointing Finger (only index up) ---
        if index_up and not middle_up and not ring_up and not pinky_up:
            return "Pointing Finger"

        # --- Victory / Peace (index + middle up) ---
        if index_up and middle_up and not ring_up and not pinky_up:
            return "Victory Sign"

        # --- Three Fingers (index + middle + ring) ---
        if index_up and middle_up and ring_up and not pinky_up:
            return "Three Fingers"

        # --- Thumbs Up (only thumb up, fist otherwise) ---
        if thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
            return "Thumbs Up"

        # --- Thumbs Down (thumb down, fist) ---
        # When thumb tip is clearly below wrist
        if lm[4].y > lm[0].y + 0.05 and not index_up and not middle_up and not ring_up and not pinky_up:
            return "Thumbs Down"

        # --- Rock Sign (index + pinky up, middle + ring down) ---
        if index_up and not middle_up and not ring_up and pinky_up:
            return "Rock Sign"

        return "Unknown"
