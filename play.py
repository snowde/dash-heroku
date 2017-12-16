import good_morning as gm
kr = gm.KeyRatiosDownloader()
kr_frames = kr.download("CMG")
print(kr_frames)