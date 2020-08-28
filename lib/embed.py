from discord import Embed


class Error(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ctx = kwargs.pop('ctx', None)
        if ctx is not None:
            self.timestamp = ctx.message.created_at

        self.color = 0xFF5252


class Success(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ctx = kwargs.pop('ctx', None)
        if ctx is not None:
            self.timestamp = ctx.message.created_at

        self.color = 0x4CAF50


class Default(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ctx = kwargs.pop('ctx', None)
        if ctx is not None:
            self.timestamp = ctx.message.created_at

        self.color = 0x197fd2


class Admin(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ctx = kwargs.pop('ctx', None)
        if ctx is not None:
            self.timestamp = ctx.message.created_at

        self.color = 0xFFC107


class Notice(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ctx = kwargs.pop('ctx', None)
        if ctx is not None:
            self.timestamp = ctx.message.created_at

        self.color = 0xFFC107
