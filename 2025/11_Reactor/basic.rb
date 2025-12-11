input_file = ARGV[0]

devices = File.readlines(input_file).map do |line|
  name, outputs = line.strip.split(': ', 2)
  outputs = outputs.split(' ')
  [name, outputs]
end.to_h

# Assuming there's no loop
def count_paths(devices, from = 'you', to = 'out')
  paths = 0
  devices[from].each do |output|
    paths += output == to ? 1 : count_paths(devices, output)
  end
  return paths
end

puts count_paths(devices)
