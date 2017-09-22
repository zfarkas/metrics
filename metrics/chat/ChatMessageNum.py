from ..base.QueryBase import QueryBase

class ChatMessageNum(QueryBase):

    def run(self):
        self.session.set_keyspace('ejabberd')
        pure_msg_count = 0
        real_msg_ids = set()
        msg_senders = set()
        msgs = self.session.execute('select msg_id, uuid, from_jid from caret_messages')
        for msg in msgs:
            pure_msg_count += 1
            real_msg_ids.add(msg.msg_id)
            msg_senders.add(msg.from_jid)
        return {"pure_msg_count": pure_msg_count, "uniqe_msg_id_count": len(real_msg_ids), "msg_senders_count": len(msg_senders)}
