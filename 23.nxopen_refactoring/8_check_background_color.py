import NXOpen
import NXOpen.UF
import subprocess


class NXJournal:

    def __init__(self):
        self.session = NXOpen.Session.GetSession()
        self.work_part = self.session.Parts.Work
        self.lw = self.session.ListingWindow
        self.uf_session = NXOpen.UF.UFSession.GetUFSession()
        self.python_path = "D:\\Programs\\Python\\Python35\\python.exe"
        self.script_path = "C:\\Users\\PopovAV\\Desktop\\tempWF\\Разработка\\_test_7-5-2-DONE_checkPixels.py"
        self.save_part_image_path = "C:\\temp\\view-{}.jpg"

    def check_background_color(self):
        work_views = self.work_part.ModelingViews
        bad_views = []
        for i, item in enumerate(work_views):
            layout = self.work_part.Layouts.FindObject("L1")
            layout.ReplaceView(
                self.work_part.ModelingViews.WorkView, item, True)
            item.Orient(item.Name, NXOpen.View.ScaleAdjustment.Fit)
            self.uf_session.Disp.CreateImage(
                self.save_part_image_path.format(i),
                self.uf_session.Disp.ImageFormat.BMP,
                self.uf_session.Disp.BackgroundColor.ORIGINAL
            )
            sub_proc = subprocess.Popen(
                [
                    self.python_path.format(i),
                    self.script_path,
                    self.save_part_image_path
                ]
            )
            sub_proc.wait()
            bad_color_flag = sub_proc.communicate()
            sub_proc.kill()
            self.lw.WriteLine(str(bad_color_flag))
            if bad_color_flag:
                bad_views.append(item.Name)
        if len(bad_views) == 0:
            return "Закраска фона соответствует требованиям"
        elif len(bad_views) == 1:
            return "Закраска фона {} не соответствует требованиям".format(
                "\n".join(bad_views))
        elif len(bad_views) > 1:
            return "Закраска фона не соответствует требованиям:\n{}".format(
                "\n".join(bad_views))


def main():
    app = NXJournal()
    app.lw.Open()
    app.lw.WriteLine(app.check_background_color())


if __name__ == "__main__":
    main()
