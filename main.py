#-*- coding:utf-8 -*-
from flask import Flask, request, render_template, url_for, session, send_file, flash, jsonify, __version__
from flask import redirect as redirectss
import config, os, asyncio
from flask_talisman import Talisman
from system_handler import Client, Error
import io
import zipfile
import psutil
import shutil
from sys import version

if config.Debug.debug: url = config.Debug.url
else: url = config.WebSettings.url

def redirect(location: str):
    if "https://" in location or "http://" in location: return redirectss(location)
    return redirectss(f"{url}{location}")

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
if not config.Debug.debug: Talisman(app, content_security_policy=False)

app.secret_key = b"%\xe0'\x01\xdeH\x8e\x85m|\xb3\xffCN\xc9g"

loop = asyncio.get_event_loop()

system_client = Client()

def get_dir_index(path:str) -> int:
    path_list = path.split("/")
    dir_list = str(system_client.cloud.setting_json.get("cloud_path")).split("/")
    v = 0
    for i in path_list:
        try:
            if i == dir_list[v]:
                v += 1
                continue
        except IndexError: break
        break

    return v

@app.route("/login", methods=["GET", "POST"])
async def login():
    back_url = str(request.args.get("back_url", "/"))
    if system_client.login_check: return redirect(back_url)
    if request.method == "GET": return render_template("login.html", back_url=back_url)
    else:
        input_id = request.form.get("id")
        input_password = request.form.get("password")
        try: await system_client.login(id=input_id, password=input_password)
        except Error.AlreadyLogin: return redirect(back_url)
        except Error.LoginFailed:
            flash("없는 아이디또는 비밀번호가 맞지 않습니다.")
            return redirect(request.url)
        return redirect(back_url)

@app.route('/file/download/<path:path>', methods=["GET"])
async def file_download(path: str):
    if not system_client.login_check: return redirect("/cloud")
    path_list = path.split("/")
    if str(path_list[0]) != str(system_client.cloud.setting_json.get("cloud_path")).split("/")[0]: path = f"{str(system_client.cloud.setting_json.get('cloud_path'))}/{path}"
    if not os.path.isfile(str(path)) and not os.path.isdir(str(path)): return "404", 404
    if os.path.isfile(str(path)): return send_file(path, as_attachment=True)
    else:
        def dir_fileadd(path: str, zip):
            for i in os.listdir(path):
                if os.path.isfile(path + f"/{i}"): zip.write(path + f"/{i}")
                elif os.path.isdir(path + f"/{i}"): dir_fileadd(path + f"/{i}", zip)
        dirzip = io.BytesIO()
        my_zip = zipfile.ZipFile(dirzip, 'w')
        for i in os.listdir(path):
            if os.path.isfile(path + f"/{i}"): my_zip.write(path + f"/{i}")
            elif os.path.isdir(path + f"/{i}"):
                for j in os.listdir(path + f"/{i}"):
                    if os.path.isfile(path + f"/{i}/{j}"): my_zip.write(path + f"/{i}/{j}")
                    elif os.path.isdir(path + f"/{i}/{j}"): dir_fileadd(path + f"/{i}/{j}", my_zip)
        my_zip.close()
        dirzip.seek(0)
        return send_file(dirzip, as_attachment=True, download_name=f"{path.split('/')[-1]}.zip", mimetype="application/zip")

@app.route('/file/preview/<path:path>', methods=["GET"])
async def file_preview(path: str):
    if not system_client.login_check: return redirect("/cloud")
    path_list = path.split("/")
    if str(path_list[0]) != str(system_client.cloud.setting_json.get("cloud_path")).split("/")[0]: path = f"{str(system_client.cloud.setting_json.get('cloud_path'))}/{path}"
    if not os.path.isfile(str(path)): return "404", 404
    try: data = await system_client.cloud.get_file(path)
    except Error.NotFound: return "404", 404
    if str((data.mimetype).split("/")[-1]).lower() in config.CloudSettings.preview_ban:
        flash("해당 파일은 미리 보기 할 수 없습니다.")
        return redirect("/cloud")
    return send_file(path, as_attachment=False)

@app.route("/file/delete/<path:path>", methods=["GET", "POST"])
async def cloud_file_del(path: str):
    if not system_client.login_check: return redirect("/")
    if not os.path.isfile(str(path)) and not os.path.isdir(str(path)): return "404", 404
    back_url = str(request.args.get("back_url", "/"))

    if not config.CloudSettings.del_user:
        if os.path.isfile(str(path)):
            os.remove(str(path))
            flash(f"{path.split('/')[-1]} 파일을 삭제했습니다.")
            return redirect("/cloud/" + back_url)
    if request.method == "GET": return render_template("user_auth.html", back_url="cloud/" + back_url)
    else:
        input_password = request.form.get("password")
        if not str(input_password) == config.CloudSettings.admin_password:
            flash("비밀번호가 맞지 않습니다.")
            return redirectss(request.url)
        if os.path.isfile(str(path)):
            os.remove(str(path))
            flash(f"{path.split('/')[-1]} 파일을 삭제했습니다.")
            return redirect("/cloud/" + back_url)
        else:
            shutil.rmtree(str(path))
            flash(f"{path.split('/')[-1]} 폴더을 삭제했습니다.")
            return redirect("/cloud/" + back_url)

@app.route("/logout", methods=["GET", "POST"])
async def logout():
    if not system_client.login_check: return redirect("/")
    await system_client.logout()
    return redirect("/login")

@app.route("/", methods=["GET", "POST"])
async def index():
    if not system_client.login_check: return redirect("/login")
    return render_template("index.html")

@app.route("/api/file/<path:path>", methods=["GET"])
async def api_GetFile(path: str):
    if not system_client.login_check: return jsonify({"message": "You must be logged in to enable it.", "code": 403}), 403
    try: data = await system_client.cloud.get_file(path)
    except Error.NotFound: return jsonify({"message": "File not found.", "code": 404}), 404
    server_path = (data.path).split("/")
    cloud_path = (data.path).split("/")
    if cloud_path[0] != str(system_client.cloud.setting_json.get("cloud_path")).split("/")[0]: cloud_path, server_path = f"{system_client.cloud.setting_json.get('cloud_path')}/{'/'.join(cloud_path[0:])}".split("/"), f"{system_client.cloud.setting_json.get('cloud_path')}/{'/'.join(cloud_path[0:])}".split("/")
    dir_index = get_dir_index("/".join(cloud_path))
    if "/".join(cloud_path[:dir_index]) == str(system_client.cloud.setting_json.get("cloud_path")): cloud_path[:dir_index] = "클라우드"
    if server_path[0] == ".": server_path[0] = "/".join(str(os.path.dirname(os.path.realpath(__file__))).split("\\"))
    return jsonify({
        "cloud_path": "/".join(cloud_path).replace("클/라/우/드", "클라우드"),
        "server_path": "/".join(server_path),
        "name": data.name,
        "bytes": data.bytes,
        "bytes_str": data.bytes_str2,
        "access_time": data.access_time,
        "make_time": data.make_time,
        "revise_time": data.revise_time,
        "access_time_str": data.access_time_str,
        "make_time_str": data.make_time_str,
        "revise_time_str": data.revise_time_str,
        "mimetype": data.mimetype,
        "type": data.type,
        "preview_ban": str((data.mimetype).split("/")[-1]).lower() in config.CloudSettings.preview_ban
    })

@app.route("/api/directory/<path:path>", methods=["GET"])
@app.route("/api/directory", methods=["GET"])
async def api_GetDirectory(path: str = None):
    if not system_client.login_check: return jsonify({"message": "You must be logged in to enable it.", "code": 403}), 403
    if path == None: path = system_client.cloud.setting_json.get("cloud_path")
    try: data = await system_client.cloud.get_directory(path)
    except Error.NotFound: return jsonify({"message": "Directory not found.", "code": 404}), 404
    server_path = (data.path).split("/")
    cloud_path = (data.path).split("/")
    if cloud_path[0] != str(system_client.cloud.setting_json.get("cloud_path")).split("/")[0]: cloud_path, server_path = f"{system_client.cloud.setting_json.get('cloud_path')}/{'/'.join(cloud_path[0:])}".split("/"), f"{system_client.cloud.setting_json.get('cloud_path')}/{'/'.join(cloud_path[0:])}".split("/")
    dir_index = get_dir_index("/".join(cloud_path))
    if "/".join(cloud_path[:dir_index]) == str(system_client.cloud.setting_json.get("cloud_path")): cloud_path[:dir_index] = "클라우드"
    if server_path[0] == ".": server_path[0] = "/".join(str(os.path.dirname(os.path.realpath(__file__))).split("\\"))
    return jsonify({
        "cloud_path": "/".join(cloud_path).replace("클/라/우/드", "클라우드"),
        "server_path": "/".join(server_path),
        "name": data.name,
        "bytes": data.bytes,
        "bytes_str": data.bytes_str2,
        "make_time": data.make_time,
        "make_time_str": data.make_time_str,
        "type": data.type,
        "file_len": len(data.files)
    })

@app.route("/api/cloud/upload", methods=["POST"])
async def cloud_file_upload():
    if not system_client.login_check: return jsonify({"message": "You must be logged in to enable it.", "code": 403}), 403
    back_url = str(request.args.get("back_url", "/"))
    path_url = str(request.args.get("path_url", "/"))
    f = request.files['file']
    add_filename = ""
    if os.path.isfile(system_client.cloud.setting_json.get("cloud_path") + f"/{path_url}/" + ".".join(f.filename.split('.')[:-1]) + add_filename + f".{f.filename.split('.')[-1]}"):
        v = 1
        while True:
            if not os.path.isfile(system_client.cloud.setting_json.get("cloud_path") + f"{path_url}/" + ".".join(f.filename.split('.')[:-1]) + f"({v})" + f".{f.filename.split('.')[-1]}"): break
            v += 1
        add_filename = f"({v})"
    f.save(system_client.cloud.setting_json.get("cloud_path") + f"/{path_url}/" + ".".join(f.filename.split('.')[:-1]) + add_filename + f".{f.filename.split('.')[-1]}")
    save_filename = ".".join(f.filename.split('.')[:-1]) + add_filename + f".{f.filename.split('.')[-1]}"
    flash(f"{save_filename} 파일이 업로드 되었습니다.")
    return redirect("/cloud/" + back_url)

@app.route("/cloud/", methods=["GET", "POST"])
@app.route("/cloud/<path:path>", methods=["GET", "POST"])
async def cloud_index(path: str = None):
    if not system_client.login_check: return redirect(f"/login?back_url=/cloud/{path or ''}")
    try: data = await system_client.cloud.get_files(path)
    except Error.NotFound: return "404"
    if path != None: path = "클라우드/" + path

    path_i = (path or "클라우드")
    path_i_list = path_i.split("/")
    if len(path_i_list) > 1:
        path_s = []
        for i in path_i_list:
            if i == "클라우드" and path_i_list.index(i) == 0:
                path_s.append("<a class='hover:bg-gray-100 hover:px-1 hover:py-0.5 transition-all duration-200 rounded-lg' href='/cloud/'>클라우드</a>")
                continue
            elif (path_i_list.index(i) + 1) == len(path_i_list):
                path_s.append(i)
                break
            path_s.append((f"<a class='hover:bg-gray-100 transition-all duration-200 rounded-lg hover:px-1 hover:py-0.5' href='/cloud/{('/'.join(path_i_list[:(path_i_list.index(i) + 1)])).replace('클라우드', '/')}'>{i}</a>").replace("//", ""))
        path_i = " / ".join(path_s)

    url_path = (path or "/").split("/")
    if url_path[0] == "클라우드": del url_path[0]

    return render_template("cloud/file_list.html", path=path_i, title_path=path or "클라우드", url_path="/".join(url_path), files=data, files_len = len(data))

@app.route("/system", methods=["GET", "POST"])
async def system_index():
    if not system_client.login_check: return redirect(f"/login?back_url=/system")

    cloud_path_list = str(system_client.cloud.setting_json.get("cloud_path")).split("/")
    if cloud_path_list[0] == ".": cloud_path_list[0] = "/".join(str(os.path.dirname(os.path.realpath(__file__))).split("\\"))
    cloud_path_list2 = ("/".join(cloud_path_list)).split("/")[0]
    try: disk = psutil.disk_usage(path=str(cloud_path_list2))
    except: pass

    cloud_disk = dict()
    cloud_disk["return"] = True

    try: disk
    except NameError: cloud_disk["return"] = False
    else:
        cloud_disk["use_percent"] = str(disk.percent) + "%"
        cloud_disk["use_percent_int"] = disk.percent
        cloud_disk["total"] = str(system_client._byte_transform(disk.total, "g", 2)) + "GB"
        cloud_disk["use"] = str(system_client._byte_transform(disk.used, "g", 2)) + "GB"
        cloud_disk["free"] = str(system_client._byte_transform(disk.free, "g", 2)) + "GB"

    system_data = {
        "client_var": f"{config.Debug.version} ({config.Debug.version_day})",
        "python_var": version.split(' ')[0],
        "flask_var": __version__,
    }
    return render_template("system/index.html", cloud_disk = cloud_disk, system_data=system_data)

@app.route("/system/reboot", methods=["GET", "POST"])
async def system_reboot():
    if not system_client.login_check: return redirect("/")
    back_url = str(request.args.get("back_url", ""))

    if request.method == "GET": return render_template("user_auth.html", back_url=back_url)
    else:
        input_password = request.form.get("password")
        if not str(input_password) == config.CloudSettings.admin_password:
            flash("비밀번호가 맞지 않습니다.")
            return redirectss(request.url)
        os.system('shutdown -r -f -t 0')

        return render_template("system/reboot.html")

@app.route("/system/shutdown", methods=["GET", "POST"])
async def system_shutdown():
    if not system_client.login_check: return redirect("/")
    back_url = str(request.args.get("back_url", ""))

    if request.method == "GET": return render_template("user_auth.html", back_url=back_url)
    else:
        input_password = request.form.get("password")
        if not str(input_password) == config.CloudSettings.admin_password:
            flash("비밀번호가 맞지 않습니다.")
            return redirectss(request.url)
        os.system('shutdown -s -f -t 0')

        return render_template("system/shutdown.html")


if config.Debug.debug: app.run(config.Debug.open_url, port=config.Debug.port, debug=True)
else: app.run(config.WebSettings.open_url, port=config.WebSettings.port)