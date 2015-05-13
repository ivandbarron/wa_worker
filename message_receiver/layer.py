from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
import threading
import logging


class SendLayer(YowInterfaceLayer):
    PROP_MESSAGES = "org.openwhatsapp.yowsup.prop.sendclient.queue"

    def __init__(self):
        super(SendLayer, self).__init__()
        self.ackQueue = []
        self.lock = threading.Condition()

    @ProtocolEntityCallback("success")
    def onSuccess(self, successProtocolEntity):
        try:
            self.lock.acquire()
            for target in self.getProp(self.__class__.PROP_MESSAGES, []):
                #getProp() is trying to retreive the list of (jid, message) tuples, if none exist, use the default []
                phone, message = target
                messageEntity = TextMessageProtocolEntity(message, to = "%s@s.whatsapp.net" % phone)
                #append the id of message to ackQueue list
                #which the id of message will be deleted when ack is received.
                self.ackQueue.append(messageEntity.getId())
                self.toLower(messageEntity)
        finally:
            self.lock.release()

    #after receiving the message from the target number, target number will send a ack to sender(us)
    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        try:
            self.lock.acquire()
            #if the id match the id in ackQueue, then pop the id of the message out
            if entity.getId() in self.ackQueue:
                self.ackQueue.pop(self.ackQueue.index(entity.getId()))
            if not len(self.ackQueue):
                self.lock.release()
                logging.info("Message was sent")
                raise KeyboardInterrupt()
        finally:
            self.lock.release()

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        try:
            self.lock.acquire()
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                'Celular de guardia, contacte a sistemas',
                to = messageProtocolEntity.getFrom())
            self.toLower(receipt)
            self.toLower(outgoingMessageProtocolEntity)
        finally:
            self.lock.release()

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        try:
            self.lock.acquire()
            ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery", entity.getFrom())
            self.toLower(ack)
        finally:
            self.lock.release()
