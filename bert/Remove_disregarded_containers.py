from pathlib import Path
import pickle

def main():
    input_dir = "../sample_data/BertContainers/"
    output_dir = "../sample_data/BertContainers_dropped_disregarded/"

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    suffix = ".pkl"
    paths = []
    for path in input_dir.glob(f'*{suffix}'):
        paths.append(path)
    for path in paths:
        print(path)
        with path.open("rb") as pkl_file:
            try:
                info_note = pickle.load(pkl_file)
            except:
                continue

        anno_set = set()
        for annot in info_note[0].annot:
            anno_set.add(annot.label)

        # Skip file if it has "disregard_file" label in the first sentence
        if "disregard\\_file" in anno_set:
            continue

        filename_out = output_dir / path.name
        with path.open('wb') as outfile:
            pickle.dump(info_note, outfile)


if __name__ == "__main__":
    main()
