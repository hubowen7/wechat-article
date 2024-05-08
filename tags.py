from enum import Enum

class Tag(Enum):
    """
    微信公众号所带标签的枚举类，用于存储理想的tags。
    """
    # 1、智驾相关技术
    BEV = "BEV"
    TRANSFORMER = "Transformer"
    BEV_TRANSFORMER = "BEV与Transformer"
    END_TO_END = "端到端"
    LARGE_MODEL = "大模型"
    GPT = "GPT"
    FSD = "FSD"
    NOA = "NOA"
    SENSOR_TECHNOLOGY = "传感器技术"
    ARTIFICIAL_INTELLIGENCE = "人工智能"
    UPPER_AI = "AI"
    AI = "ai"
    LIDAR = "激光雷达"
    AI_CHIP = "AI芯片"
    CHIP = "芯片"
    DEEP_LEARNING = "深度学习"
    COMPUTER_VISION = "计算机视觉"

    # 2、智驾衍生名词
    AUTO_DRIVING = "自动驾驶"
    SMART_DRIVING = "智能驾驶"
    S_D = "智驾"
    DRIVING = "行车"
    PARKING = "泊车"
    SMART_CAR = "智能汽车"
    AUTONOMOUS_VEHICLES = "自动驾驶车辆"
    INTELLIGENT = "智能化"

    # 3、智驾相关公司
    TESLA = "特斯拉"
    HORIZON = "地平线"
    CAMBRIAN = "寒武纪"
    MOMENTA = "Momenta"
    WE_RIDE = "文远"
    PONY = "小马"
    WE_RIDE_AI = "文远知行"
    PONY_AI = "小马智行"