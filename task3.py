def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals['lesson']
    pupil = intervals['pupil']
    tutor = intervals['tutor']

    def merge_intervals(intervals: list[int]) -> list[list[int]]:
        if not intervals:
            return []
        # Разбиваем список на пары
        it = iter(intervals)
        pairs = list(zip(it, it))
        # Сортируем по началу интервала
        sorted_pairs = sorted(pairs, key=lambda x: x[0])
        merged = []
        for start, end in sorted_pairs:
            if not merged:
                merged.append([start, end])
            else:
                last_start, last_end = merged[-1]
                if start <= last_end:
                    # Перекрытие или соприкосновение, объединяем
                    new_start = last_start
                    new_end = max(last_end, end)
                    merged[-1] = [new_start, new_end]
                else:
                    merged.append([start, end])
        return merged

    def intersect_with_lesson(merged_intervals, lesson_start, lesson_end):
        result = []
        for start, end in merged_intervals:
            current_start = max(start, lesson_start)
            current_end = min(end, lesson_end)
            if current_start < current_end:
                result.append([current_start, current_end])
        return result

    # Объединяем интервалы ученика и учителя
    merged_pupil = merge_intervals(pupil)
    merged_tutor = merge_intervals(tutor)

    # Обрезаем по уроку
    lesson_start, lesson_end = lesson
    pupil_in_lesson = intersect_with_lesson(
        merged_pupil, lesson_start, lesson_end
        )
    tutor_in_lesson = intersect_with_lesson(
        merged_tutor, lesson_start, lesson_end
        )

    # Находим пересечения интервалов ученика и учителя в рамках урока
    total_time = 0
    i = j = 0
    while i < len(pupil_in_lesson) and j < len(tutor_in_lesson):
        pupil_start, pupil_end = pupil_in_lesson[i]
        tutor_start, tutor_end = tutor_in_lesson[j]

        # Находим пересечение текущих интервалов
        overlap_start = max(pupil_start, tutor_start)
        overlap_end = min(pupil_end, tutor_end)
        if overlap_start < overlap_end:
            total_time += overlap_end - overlap_start

        # Переходим к следующему интервалу, который заканчивается раньше
        if pupil_end < tutor_end:
            i += 1
        else:
            j += 1

    return total_time
