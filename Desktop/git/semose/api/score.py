def distance_weight(distance):
    sector_1 = 1
    sector_2 = 0.7
    sector_3 = 0.1
    sector_4 = 0

    m_1 = 1
    m_2 = 10
    m_3 = 20
    m_4 = 30

    if distance <= m_1:
        return sector_1
    elif distance <= m_2:
        # 제곱 또는 세제곱 등 다항식으로 변경하여 가파르게 설정할 수 있습니다.
        return sector_1 + ((distance - m_1) / (m_2 - m_1)) * (sector_2 - sector_1)
    elif distance <= m_3:
        return sector_2 + ((distance - m_2) / (m_3 - m_2)) * (sector_3 - sector_2)
    elif distance <= m_4:
        return sector_3 + ((distance - m_3) / (m_4 - m_3)) * (sector_4 - sector_3)
    else:
        return 0

print(distance_weight(29))