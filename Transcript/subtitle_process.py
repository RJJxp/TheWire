import io
import os
import sys

class SubElement(object):
    time_stamp_start = []
    time_stamp_end = []
    cn_subtitle = []
    en_subtitle = []

    def __init__(self):
        pass
    
    # check ele
    def checkEle(self):
        assert (len(self.cn_subtitle) == len(self.en_subtitle))
        assert (len(self.en_subtitle) == len(self.time_stamp_start))
        assert (len(self.time_stamp_start) == len(self.time_stamp_end))
        print("There is %d subtitles" %len(self.cn_subtitle))

    def printEle(self):
        for i in range(len(self.cn_subtitle)):
            print("No.%06d" %i)
            print("Time Stamp:")
            print("%s -- %s" %(self.time_stamp_start[i], self.time_stamp_end[i]))
            print("EN: %s" %self.en_subtitle[i])
            print("CN: %s" %self.cn_subtitle[i])

    def testInFile(self):
        output_lines = []
        for i in range(len(self.cn_subtitle)):
            output_line = ""
            output_line = output_line + ("%s == %s" %(self.time_stamp_start[i], self.time_stamp_end[i])) + "\n"
            output_line = output_line + self.en_subtitle[i] + "\n" + self.cn_subtitle[i] + "\n\n"
            output_lines.append(output_line)
        with open("testttt.txt", 'w', encoding="utf-8") as f1:
            f1.writelines(output_lines)
    print("Finished writing.")
            

class SubtitleProcess(object):
    # input param
    __sub_type = ""
    __input_path = ""
    __output_dir = ""
    __split_key = ""
    __ignore_key = None
    # output param
    __ele = SubElement()

    def __init__(self):    
        pass

    # decorate of __input_path
    @property
    def input_path(self):
        return self.__input_path
    @input_path.setter
    def input_path(self, input_path__):
        self.__input_path = input_path__

    # decarate of __output_dir
    @property
    def output_dir(self):
        return self.__output_dir
    @output_dir.setter
    def output_dir(self, output_dir__):
        self.__output_dir = output_dir__

    # decarate of __sub_tpye
    @property
    def sub_type(self):
        return self.__sub_type
    @sub_type.setter
    def sub_type(self, sub_tpye__):
        self.__sub_type = sub_tpye__

    # interface 
    def getLaTeXCommand(self):
        self.__process_sub_file()
        LaTeX_str = self.__generateLaTeX()
        self.__writeLaTeX(LaTeX_str)

    # Private Function
    # process the subtitle file according to the sub type
    def __process_sub_file(self):
        if self.__sub_type == "the_wire":
            self.__split_key = r"\N{\fnMicrosoft YaHei\fs14\2c&H111211&}"
            # self.__split_key = r"\N{\fs14}"
            self.__ignore_key = [r"{\fs14}", r"{\fs16}", r"{\r}", r"{\an8}", r"{\fs17}", r"{\fs15}", r"{\fs18}"]
            self.__processTheWireSubs()
        else:
            print("Please enter the right sub type.")
    
    def __processTheWireSubs(self):
        with open(self.__input_path, 'r', encoding="utf-16le") as f1:
            for f_line in f1.readlines():
                if f_line[0:8] != "Dialogue":
                    continue

                s = f_line[63:]
                key_idx = s.find(self.__split_key)
                if key_idx == -1:
                    continue
                key_len = len(self.__split_key)
                cn_sub_origin = s[0:key_idx]
                en_sub_origin = s[key_idx+key_len:].strip("\n")
                cn_sub = cn_sub_origin
                en_sub = en_sub_origin
                for ignore_key in self.__ignore_key:
                    cn_sub = cn_sub.replace(ignore_key, "")
                    en_sub = en_sub.replace(ignore_key, "")
                time_start = f_line[12:22]
                time_end = f_line[23:33]
                self.__ele.cn_subtitle.append(cn_sub)
                self.__ele.en_subtitle.append(en_sub)
                self.__ele.time_stamp_start.append(time_start)
                self.__ele.time_stamp_end.append(time_end)
            
            self.__ele.checkEle()
            # self.__ele.printEle()
            self.__ele.testInFile()
            print("finished processTheWireSubs().")
            
    def __generateLaTeX(self):
        if self.__sub_type == "the_wire":
            return self.__generateTheWireLaTeX()
        else:
            print("Please enter the right sub type.")
        
    def __generateTheWireLaTeX(self):
        LaTeX_str = []
        for ts, te, cn, en in zip(self.__ele.time_stamp_start, self.__ele.time_stamp_end, self.__ele.cn_subtitle, self.__ele.en_subtitle):
            # take the non "-" content of cn, en 
            if (cn[0:1] == "-" and en[0:1] == "-"):
                cn_content = cn.split("-")[1:]
                en_content = en.split("-")[1:]
            else:
                cn_content = [cn]
                en_content = [en]
            # generate the LaTeX
            # cn part
            single_str = "\\switchcolumn*" + "\n"
            single_str = single_str + ("\\texttt{%s -- %s}" %(ts, te)) + "\n\n"
            for i in range(len(cn_content)):
                cnn = cn_content[i]
                cnn = cnn.strip(" ")

                cnn = cnn.replace("%",r"\%")
                cnn = cnn.replace("&",r"\&")

                single_str = single_str + ("\\textit{- %s}" %cnn)
                if i == (len(cn_content) - 1):
                    single_str = single_str + "\n" + "\\newline"    
                    single_str = single_str + "\n\n"
                else: 
                    single_str = single_str + "\n\n"
            # en part
            single_str = single_str + "\\switchcolumn" + "\n"
            single_str = single_str + ("\\texttt{%s -- %s}" %(ts, te)) + "\n\n"
            for i in range(len(en_content)):
                enn = en_content[i]
                enn = enn.strip(" ")
                enn = enn.strip("\n")
                # replace `$` with `\$`, dollar
                enn = enn.replace("$", r"\$")
                enn = enn.replace("%", r"\%")
                enn = enn.replace("&", r"\&")

                single_str = single_str + ("\\textsf{- %s}" %enn)
                if i == (len(cn_content) - 1):
                    single_str = single_str + "\n" + "\\newline"    
                    single_str = single_str + "\n\n"
                else: 
                    single_str = single_str + "\n\n" 

            LaTeX_str.append(single_str)

        print("There is %d subtitles." %len(LaTeX_str))
        return LaTeX_str

    def __writeLaTeX(self, LaTeX_str):
        filename = os.path.basename(self.input_path)[:-4]
        output_path = self.output_dir + filename + ".tex"
        with open(output_path, 'w', encoding="utf-8") as f1:
            f1.writelines(LaTeX_str)
        print("Finished writing.")