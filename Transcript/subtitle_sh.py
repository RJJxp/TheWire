import os 
import shutil

input_dir = r"D:\下载\115\theWireSubtitle\The Wire WEBDL"
output_dir = r"C:\Users\rjjjj\Desktop\TheWire\Transcript\from_ass"

command_list = []
all_files = os.listdir(input_dir)
for ass_file in all_files:
    ass_file_path = os.path.join(input_dir, ass_file)
    command_str = "python subtitle.py --input-path \"%s\" --output-dir \"%s\"" %(ass_file_path, output_dir)
    command_list.append(command_str)

for com in command_list:
    os.system(com)
    print("\n")

print("===========================")
print("Finished Generate Para-col TeX Part.")
print("===========================")

print("===========================")
print("Start Main TeX Part.")
print("===========================")

all_paracol_files = os.listdir(output_dir)
main_tex_output_dir = r"C:\Users\rjjjj\Desktop\TheWire\Transcript"
se_list = []
for paracol_file in all_paracol_files:
    se = paracol_file[9:15]
    se_list.append(se)
    tex_file_name = paracol_file[:-4]

    main_tex_str = \
            r"\documentclass[a4paper, 12pt]{article}" + "\n\n" \
            + r"\input{chapter/envir}" + "\n\n" \
            + r"\begin{document}" + "\n\n" \
            + r"\begin{center}" + "\n" \
            + r"    {\Huge\ttfamily " + "\n" \
            + r"        The Wire \\[20pt] " + "%s" %se + r"}\\[50pt]" + "\n\n" \
            + r"    {\Large\ttfamily" + "\n" \
            + r"        Supported by \\[12pt]" + "\n" \
            + r"        \textbf{www.1000fr.net}\\[12pt]" + "\n" \
            + r"        Created by \\[12pt]" + "\n" \
            + r"        \textbf{RJJxp}\\[12pt]" + "\n" \
            + r"        2021-06-27}" + "\n" \
            + r"\end{center}" + "\n" \
            + r"\thispagestyle{empty}" + "\n\n" \
            + r"\newpage" +"\n" \
            + r"\pagenumbering{arabic}" + "\n" \
            + r"\begin{paracol}{2}" + "\n" \
            + r"    \input{from_ass/" + "%s" %tex_file_name + r"}" + "\n" \
            + r"\end{paracol}" + "\n" \
            + r"\end{document}"
            
    main_tex_output_path = os.path.join(main_tex_output_dir, se + ".tex")
    with open(main_tex_output_path, 'w', encoding="utf-8") as f1:
        f1.writelines(main_tex_str)
print("===========================")
print("End Main TeX Part.")
print("===========================")

print("===========================")
print("Start Building TeX.")
print("===========================")
now_workdir = os.getcwd()
print(now_workdir)
os.chdir(main_tex_output_dir)
for se in se_list:
    LaTeX_command = "xelatex -synctex=1 -interaction=nonstopmode -file-line-error %s.tex" %se    
    # os.system(LaTeX_command)
print("===========================")
print("End Building TeX.")
print("===========================")

# # move the pdf to folder
# for se in se_list:
#     src_file_path = se + ".pdf"
#     tgt_file_path = "pdf\\" + "%s" %se + ".pdf"
#     shutil.move(src_file_path, tgt_file_path)
#     print("Move %s --> %s") %(src_file_path, tgt_file_path)

# # remove the mid files
# all_files_in_LaTeX = os.listdir(main_tex_output_dir)
# for LaTeX_file in all_files_in_LaTeX:
#     if (LaTeX_file[0] == "S" and LaTeX_file[3] == "E" and LaTeX_file[:-4] != ".pdf"):
#         os.remove(os.path.join(main_tex_output_dir, LaTeX_file))
#         print("remove %s" %LaTeX_file)

# back to origin work dir
os.chdir(now_workdir)







