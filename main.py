import random
import os


def extract_LCSTS(origin, is_partI=False):
    if is_partI:
        tmp = 0
    else:
        tmp = 1

    summaries = []
    articles = []

    with open(origin) as f_origin:
        lines = f_origin.read().splitlines()
        for i in range(0, len(lines), 8+tmp):
            if not is_partI:
                score_line = lines[i+1].strip()
                if int(score_line[13]) < 3:
                    continue
            summaries.append(lines[i+2+tmp].strip())
            articles.append(lines[i+5+tmp].strip())

    return articles, summaries

def save_data(x, y, output_dir, prefix):
    with open("{}/{}.target".format(output_dir, prefix), 'w') as tgt_output, open("{}/{}.source".format(output_dir, prefix), 'w') as src_output:
        tgt_output.write('\n'.join(y))
        src_output.write('\n'.join(x))


def main():
    # Arguments
    PART_I_data = '../../LCSTS2.0/DATA/PART_I.txt'
    PART_III_data = '../../LCSTS2.0/DATA/PART_III.txt'
    output_dir = './clean_data/'

    # Extract data
    partI_x, partI_y = extract_LCSTS(PART_I_data, is_partI=True)
    partIII_x, partIII_y = extract_LCSTS(PART_III_data)

    # Remove overlapping data
    overlap_cnt = 0

    clean_partI_x = []
    clean_partI_y = []

    for idx in range(len(partI_x)):
        if partI_y[idx] in partIII_y:
            overlap_cnt += 1
        else:
            clean_partI_x.append(partI_x[idx])
            clean_partI_y.append(partI_y[idx])

    dirname = os.path.dirname(output_dir)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    save_data(partIII_x, partIII_y, output_dir, 'test')
    save_data(clean_partI_x, clean_partI_y, output_dir, 'train')

    print("Remove {} pairs".format(overlap_cnt))

if __name__ == '__main__':
    main()
