from pythonosc import dispatcher
from pythonosc import osc_server
import statusLoop

class OscServer:

    def connect(self, client, loops):
        self.loops = loops
        dispatchero = dispatcher.Dispatcher()
        dispatchero.map("/statusChanged", self.handleStatusChange)
        dispatchero.map("/loopPosChanged", self.handleLoopPosChange)
        dispatchero.map("/loopLenChanged", self.handleLoopLenChange)

        server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 9952), dispatchero)

        self.registerCallbacks(client)

        statusGetter = statusLoop.StatusLoop(loops, client)
        statusGetter.start()

        server.serve_forever()

    def handleStatusChange(self, path, index, control, value):
        self.loops[index].setLoopStatus(value)

    def handleLoopPosChange(self, path, index, control, value):
        self.loops[index].setLoopPos(value)

    def handleLoopLenChange(self, path, index, control, value):
        self.loops[index].setLoopLen(value)

    def registerCallbacks(self, client):
        for i,loop in enumerate(self.loops):
            #client.send_message("/sl/"+str(i)+"/register_update",["state", "127.0.0.1:9952", "/statusChanged"])
            client.send_message("/sl/"+str(i)+"/register_auto_update",["loop_pos", 100, "127.0.0.1:9952", "/loopPosChanged"])
            client.send_message("/sl/"+str(i)+"/register_auto_update",["loop_len", 100, "127.0.0.1:9952", "/loopLenChanged"])