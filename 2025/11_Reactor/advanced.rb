input_file = ARGV[0]

devices = File.readlines(input_file).map do |line|
  name, outputs = line.strip.split(': ', 2)
  outputs = outputs.split(' ')
  [name, outputs]
end.to_h

def count_paths(devices, cache, from:, to: 'out')
  return 0 unless devices.has_key?(from)
  return cache[[from, to]] if cache.has_key?([from, to])
  paths = 0
  devices[from].each do |output|
    paths += output == to ? 1 : count_paths(devices, cache, from: output, to: to)
  end
  cache[[from, to]] = paths
  return paths
end

cache = Hash.new
svr_fft = count_paths(devices, cache, from: 'svr', to: 'fft')
fft_dac = count_paths(devices, cache, from: 'fft', to: 'dac')
dac_out = count_paths(devices, cache, from: 'dac', to: 'out')

puts svr_fft * fft_dac * dac_out
