from aiogram.dispatcher.filters.state import State, StatesGroup


class OrmPanel(StatesGroup):
    main = State()


class CreateTable(StatesGroup):
    table_name = State()
    column_name = State()
    column_type = State()
    continue_or_not = State()
