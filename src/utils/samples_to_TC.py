def samples_to_TC(timeref, sample_rate):
  hours = timeref / sample_rate / 3600
  mins = (timeref / sample_rate) % 3600 / 60
  seconds = (timeref / sample_rate) % 60
  frames = (timeref / sample_rate) % 1
  if frames < 10: frames = f"0{frames}"
  return f"{hours}:{mins}:{seconds}:{frames}"
