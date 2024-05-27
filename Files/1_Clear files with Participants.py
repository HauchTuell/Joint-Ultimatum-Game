p1path = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\P1Response.txt"
p2path = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\P2Response.txt"
offer_path = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\Offer.txt"
offer_path2 = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\Offer2.txt"
dec_path = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\Decision.txt"
dec_path2 = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\Decision2.txt"
r_path = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\ready.txt"
r2_path = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\ready2.txt"
r3_path = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\ready3.txt"
r4_path = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\ready4.txt"
part_file = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\part_file.txt"
part_file2 = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\part_file2.txt"

paths = [p1path, p2path, offer_path, offer_path2, dec_path, dec_path2, r_path, r2_path, r3_path, r4_path, part_file, part_file2]

for i in paths:
    with open (i, 'w') as f:
        pass
        f.close()


# def participant_numbers(part_file):
#     # Reading the file
#     with open(part_file, "r+") as file:
#         print('yes')
#         lines = file.readlines()
#         if not lines:
#             last_row = 0  # If the file is empty, start from 0
#         if lines:
#             last_row = lines[-1]
#         # Extracting the number from the last row
#         if last_row == 0:
#             file.write("Participant_1\n")
#             print("Participant_1")
#         else:
#             last_number = int(last_row.split("_")[1].strip())
#             current_number = last_number + 1
#             # Writing the new row with the next number
#             file.write(f"Participant_{current_number}\n")
#             print(current_number)
# participant_numbers(part_file)