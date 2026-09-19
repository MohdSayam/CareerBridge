from flask_socketio import SocketIO, join_room, leave_room, emit
import logging

socketio = SocketIO()

# Track who is in each room: room_id -> list of session IDs
rooms = {}

def register_socket_handlers(sio):
    
    @sio.on("connect")
    def handle_connect():
        logging.info(f"Client connected: {sio.sid if hasattr(sio, 'sid') else 'unknown'}")

    @sio.on("disconnect")
    def handle_disconnect():
        # Clean up rooms on disconnect
        sid = None
        try:
            from flask import request
            sid = request.sid
        except Exception:
            pass

        if sid:
            for room_id in list(rooms.keys()):
                if sid in rooms[room_id]:
                    rooms[room_id].remove(sid)
                    # Notify the remaining peer
                    emit("peer_disconnected", {"sid": sid}, room=room_id, skip_sid=sid)
                    if not rooms[room_id]:
                        del rooms[room_id]
                    break

    @sio.on("join_interview")
    def handle_join(data):
        from flask import request
        room_id = str(data.get("room_id"))
        role = data.get("role", "unknown")
        sid = request.sid

        join_room(room_id)

        if room_id not in rooms:
            rooms[room_id] = []

        rooms[room_id].append(sid)

        peer_count = len(rooms[room_id])
        logging.info(f"[Room {room_id}] {role} joined. Total peers: {peer_count}")

        # Tell the joining peer how many people are already in the room
        emit("room_joined", {
            "room_id": room_id,
            "peer_count": peer_count,
            "should_initiate": peer_count == 2  # Second peer to join initiates the offer
        })

        # Notify others that a new peer joined
        if peer_count > 1:
            emit("peer_joined", {"sid": sid, "role": role}, room=room_id, skip_sid=sid)

    @sio.on("webrtc_offer")
    def handle_offer(data):
        from flask import request
        room_id = str(data.get("room_id"))
        emit("webrtc_offer", {
            "sdp": data.get("sdp"),
            "from_sid": request.sid
        }, room=room_id, skip_sid=request.sid)

    @sio.on("webrtc_answer")
    def handle_answer(data):
        from flask import request
        room_id = str(data.get("room_id"))
        emit("webrtc_answer", {
            "sdp": data.get("sdp"),
            "from_sid": request.sid
        }, room=room_id, skip_sid=request.sid)

    @sio.on("ice_candidate")
    def handle_ice(data):
        from flask import request
        room_id = str(data.get("room_id"))
        emit("ice_candidate", {
            "candidate": data.get("candidate"),
            "from_sid": request.sid
        }, room=room_id, skip_sid=request.sid)

    @sio.on("leave_interview")
    def handle_leave(data):
        from flask import request
        room_id = str(data.get("room_id"))
        sid = request.sid

        leave_room(room_id)
        if room_id in rooms and sid in rooms[room_id]:
            rooms[room_id].remove(sid)
            if not rooms[room_id]:
                del rooms[room_id]

        emit("peer_disconnected", {"sid": sid}, room=room_id)
        logging.info(f"[Room {room_id}] Peer {sid} left.")
