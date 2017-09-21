from ..base.QueryBase import QueryBase

class ChatMessageNum(QueryBase):

    def run(self):
        self.session.set_keyspace('ejabberd')
        pure_msg_count = 0
        real_msg_ids = set()
        msgs = self.session.execute('select msg_id, uuid from caret_messages')
        for msg in msgs:
            pure_msg_count += 1
            real_msg_ids.add(msg.msg_id)
        return {"pure_msg_count": pure_msg_count, "uniqe_msg_id_count": len(real_msg_ids)}
