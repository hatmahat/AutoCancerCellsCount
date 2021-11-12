import celltypes as ct

DIRR = r"D:\White Blood Cells  RSUP Sardjito - Copy\working data 2\final dataset\train-val-test - Copy (2)"
CHILD = r"test-v2 (org)"

# DIRR = r"D:\White Blood Cells  RSUP Sardjito - Copy"
# CHILD = r"sampel 1 (clean)"

count = ct.CountTypes(DIRR, CHILD)
count.read_file_names()
count.count_cells()

cells = count.get_uniq_dict()
binary = count.get_blast_vs_nonblast()
print("Cell types:", cells)
print("Binary types:", binary)
print("Total cells:", binary['Limfoblas']+binary['Non-Limfoblas'])
print("Labelled imgs:", len(count.get_preprocessed()))
# i = 0
# for name in count.get_preprocessed():
#     if len(name) == 1:
#         i += 1
#         print(f"{i}:", name)