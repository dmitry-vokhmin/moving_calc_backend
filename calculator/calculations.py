_movers = {"1_bedroom": 2}
_load_unload_time = {"1_bedroom": 5}
_truck_type = {"1_bedroom": 16}
calculations_result = {}


def calculations(data):
    truck_type = 0
    default = False
    movers = None
    load_unload_time = 0
    cubic_feet = 0
    floor_factor = 1
    travel_between_load_and_unload = 0
    for key, value in data.items():
        if key == "floor_collection":
            floor_factor = 1
        elif key == "move_size":
            room_collection = []
            if "default" in room_collection:
                truck_type = _truck_type[key]
                movers = _movers[key]
                load_unload_time = _load_unload_time[key]
                default = True
            else:
                for itm in room_collection:  # У предметов есть тип, а у каждого типа есть присвоеное время
                    load_unload_time += itm
                    cubic_feet += itm
                    if itm == "type_6":
                        movers = 4  # Если предмет определенной категории ставить минимальное количество людей
                        truck_type = 26
        elif key == "services":
            if value == "loading":
                load_unload_time *= 0.1
            elif value == "unloading":
                load_unload_time *= 0.2
        elif key == "zip_code":
            office = 0
            travel_time = office + value[0] + value[1] + office
            travel_between_load_and_unload = value[0] + value[1]
    if default is False:
        movers = 1  # Load and uload time соотносится с рамками установленными по умолчанию
        # и устанавливает количество грузчиков на основе этого
        truck_type = 0  # Выбирается по границам вместимости в грузовик на основе подсчитаных cubic_feet
    move_time = load_unload_time + (load_unload_time * floor_factor) + travel_between_load_and_unload
    move_time /= movers
    estimated_move_time = [move_time, move_time + 2]
    hourly_rate = get_price_tag() * movers
    estimated_price = [estimated_move_time[0] * hourly_rate, estimated_move_time[1] * hourly_rate]
    calculations_result["estimated_hours"] = "2-4"
    calculations_result["movers"] = 2
    calculations_result["truck_type"] = 16
    calculations_result["hourly_rate"] = 120
    calculations_result["travel_time"] = 30
    calculations_result["estimated_cost"] = "240-480"
    return calculations_result


def get_price_tag():
    return 1
