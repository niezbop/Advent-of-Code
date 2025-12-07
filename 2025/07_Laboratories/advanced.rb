input_file = ARGV[0]

lines = File.readlines(input_file)

TIMELINES_CACHE = {}
def count_timelines(lines, line_index, beam_index)
  return 1 if line_index >= lines.count
  return TIMELINES_CACHE[[line_index, beam_index]] if TIMELINES_CACHE.include?([line_index, beam_index])

  char = lines[line_index][beam_index]
  timelines_count = 0
  if char == '^'
    timelines_count += count_timelines(lines, line_index + 1, beam_index - 1) + count_timelines(lines, line_index + 1, beam_index + 1)
  else
    timelines_count = count_timelines(lines, line_index + 1, beam_index)
  end

  TIMELINES_CACHE[[line_index, beam_index]] = timelines_count
  return timelines_count
end

initial_beam = lines[0].index('S')
puts count_timelines(lines, 1, initial_beam)

