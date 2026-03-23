import matplotlib.pyplot as plt

types = [
    "HTML", "Images", "Audio/Video", "JavaScript",
    "CSS", "Fonts", "Plain Text", "JSON", "DASH/HLS"
]

counts = [126, 312, 161, 435, 84, 25, 37, 431, 20]

plt.figure()
plt.bar(types, counts)

plt.xlabel("File Type")
plt.ylabel("Number of URLs")
plt.title("URLs by File Type in WARC")

plt.xticks(rotation=45)

plt.savefig("barchart.png")
plt.show()