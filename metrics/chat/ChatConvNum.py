from ..base.QueryBase import QueryBase

class ChatConvNum(QueryBase):

    def run(self):
        self.session.set_keyspace('ejabberd')
        conv = self.session.execute('select count(*) from caret_conversation')
        return {"conversation_number": conv[0].count}
