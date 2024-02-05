from aiogram.fsm.state import StatesGroup, State


class ServiceOW(StatesGroup):
    choosing_service_step_1 = State()
    choosing_service_step_2 = State()
    choosing_service_step_3 = State()
    choosing_service_step_4 = State()
    choosing_service_step_5 = State()
    choosing_service_step_6 = State()


class ServiceGM(StatesGroup):
    choosing_service_step_1 = State()
    choosing_service_step_2 = State()
    choosing_service_step_3_1 = State()
    choosing_service_step_3_2 = State()
    choosing_service_step_4_1 = State()
    choosing_service_step_4_2 = State()


