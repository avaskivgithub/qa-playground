import time, os, subprocess

def draw_gnuplot_chart(data_files_paths,
                        result_dir,
                        result_x_clmn_no=1,
                        result_y_clmn_no=2,
                        title='Results title',
                        xlable='Request X',
                        ylable='Request Y',
                        output_file='load_results.png',
                        if_rm_data_file=False):

        chart_file_path = os.path.join(result_dir, output_file)
        gnuplot_script_path = os.path.join(result_dir, 'gnuplot_load_result')

        # Create gnuplot_load_result script
        plot_args = []
        for file_path in data_files_paths:
            plot_args.append('"{}" using {}:{} title "{}" with lines'.format(file_path,
            #plot_args.append('"{}" using {}:{} title "{}" '.format(file_path,
                                                                             result_x_clmn_no,
                                                                             result_y_clmn_no,
                                                                             os.path.basename(file_path).split('.')[0]))
        gnuplot_script = """#!/usr/bin/gnuplot -persist
            set grid
            set title "{}"
            set xlabel "{}"
            set ylabel "{}"

            set terminal png size 2000,1500 enhanced font "Helvetica,20"
            set output "{}"

            plot {}
        """.format(title,
                   xlable,
                   ylable,
                   chart_file_path,
                   ','.join(plot_args))

        # Draw chart (2D plots from data in )
        cmds = ["echo '{}' > {}".format(gnuplot_script, gnuplot_script_path),
                "chmod +x {}".format(gnuplot_script_path),
                "{}".format(gnuplot_script_path),

                "rm {}".format(gnuplot_script_path)
                ]

        for cmd in cmds:
            subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            time.sleep(1)

        # Cleanup data files data_files_paths
        if if_rm_data_file:
            for file_path in data_files_paths:
                subprocess.Popen("rm {}".format(file_path), stdout=subprocess.PIPE, shell=True)
                time.sleep(1)

        print('Result chart: {}'.format(chart_file_path))

if __name__ == '__main__':

    curent_dir = data_file_path = os.path.dirname(__file__)
    data_file_path1 = os.path.join(curent_dir, 'drawdemo1.dat')
    data_file_path2 = os.path.join(curent_dir, 'drawdemo2.dat')
    files_paths = [data_file_path1, data_file_path2]

    for file_id, data_file_path in enumerate(files_paths):
        with open(data_file_path, 'w') as f:
            for i in range(10):
                f.write('{} {}\n'.format(i, (file_id + 2) ** i))

    draw_gnuplot_chart(data_files_paths=files_paths, result_dir=curent_dir,
                       output_file='data/draw_demo.png',
                       if_rm_data_file=True)

    # files_paths = ['/tmp/ab', '/tmp/ge', '/tmp/th']
    # draw_gnuplot_chart(data_files_paths=files_paths, result_dir=curent_dir,
    #                    output_file='data/draw_demo_ab_vs_gevent.png',
    #                    title='Apache Benchmark (ab) vs gevent (ge)',
    #                    ylable='Request Time Send (secs:millisecs in current hour)',
    #                    xlable='Request No',
    #                    if_rm_data_file=False)