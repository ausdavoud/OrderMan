import csv
import io


def merge_list_csv(csv_in_binary, new_rows: list[dict]):
    if csv_in_binary:
        csv_string = csv_in_binary.decode("utf-8")

        # read csv data
        with io.StringIO(csv_string) as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
    else:
        data = []

    
    data.extend(new_rows)

    # create new csv
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    output.seek(0)

    return output
