
def sub_filter(subtitles, time_start, time_end):
    filtered_subtitles = []
    for sub in subtitles:
        if sub.start > time_end:
            continue
        if sub.end < time_start:
            continue
        if sub.end >= time_start or sub.start <= time_end:
            filtered_subtitles.append(sub)
    return filtered_subtitles
