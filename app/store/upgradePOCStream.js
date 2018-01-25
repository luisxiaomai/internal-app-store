process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
(function () {
	"use strict";
	var interval = 10;

	var http = require("http")
	var https = require('https');
	var util = require("util");
	var path = require("path")
	var fs = require("fs");
	var exec = require('child_process').exec;

	//copy a file
	var copyFile = function (src, dst) {
		var is = fs.createReadStream(src);
		var os = fs.createWriteStream(dst);
		is.pipe(os);
	};

	var downloadFile = function (serverpath, localpath, callback, port) {
		var folder = localpath.substring(0, localpath.lastIndexOf('/'));
		var version = folder.substring(folder.lastIndexOf('/') + 1);
		var startDownload = function () {
			var file = fs.createWriteStream(localpath);
			var _port = "8080";
			if (port != null) {
				_port = port;
			}
			var _path = serverpath.substring(serverpath.indexOf(_port) + 4);
			var _host = serverpath.substring(serverpath.indexOf('http://') + 7, serverpath.indexOf(':' + _port));
			var req = http.request({
				hostname: _host,
				port: _port,
				path: _path
			}, function (res) {
				console.log(res.headers)
				var _len = res.headers['content-length'];
				if (_len == null) {
					console.log("can not download because the app is no longer exist");

					if (callback) callback.apply([], this);
					return;
				}
				var totalLength = Number(_len);

				var currentLength = 0;
				res.on('data', function (data) {
					currentLength += data.length;
					file.write(data);
					console.log("Downloading " + localpath.substring(localpath.lastIndexOf('/') + 1) + " Version: " + version + " ... " + ((currentLength / totalLength) * 100 + "").substring(0, 4) + "%");
				});
				res.on('end', function () {
					file.end();
					if (localpath.indexOf('apk') > 0 || localpath.indexOf('ipa') > 0) {
						console.log("Download succeed!");
						var storeFile = localpath.substring(localpath.lastIndexOf('/') + 1);
						fs.exists(storeFile, function (exists) {
							if (exists) {
								fs.unlinkSync(storeFile);
							}
							copyFile(localpath, storeFile);
						});
					}
					if (callback) callback.apply([], this);
				});
			});
			req.on('error', function (e) {
				console.log('problem with download ' + serverpath + ' : ' + e.message);
				try {
					fs.rmdirSync(folder);
				} catch (e) {
					console.log("can not download");
				}
				if (callback) callback.apply([], this);
			});
			// write data to request body
			if (localpath.indexOf('apk') < 0) {
				req.write('data\n');
				req.write('data\n');
			}
			req.end();
		};
		fs.exists(folder, function (exists) {
			if (exists) {
				startDownload();
			} else {
				var rootFolder = folder.substring(0, folder.lastIndexOf('/'));
				console.log(rootFolder);
				fs.exists(rootFolder, function (exists) {
					console.log(exists);
					if (!exists) {
						var mkdir = 'mkdir ' + rootFolder;
						console.log(mkdir);
						exec(mkdir, function (err, stdout, stderr) {
							if (err) {
								console.log("can not create root folder " + err);
								if (callback) callback.apply([], this);
							} 
						});
					}
					var mkdir = 'mkdir ' + folder;
					exec(mkdir, function (err, stdout, stderr) {
						if (err) {
							console.log("can not create folder " + err);
							if (callback) callback.apply([], this);
						} else {
							startDownload();
						}
					});
					
				});
			}
		
		});
	};
var downloadHttpsFile = function (serverpath, localpath, callback, port) {
	var folder = localpath.substring(0, localpath.lastIndexOf('\\'));
	var version = folder.substring(folder.lastIndexOf('\\') + 1);
	var startDownload = function () {
		var file = fs.createWriteStream(localpath);
		var _port = "8443";
		if (port != null) {
			_port = port;
		}
		var _path = serverpath.substring(serverpath.indexOf(_port) + 4);
		var _host = serverpath.substring(serverpath.indexOf('https://') + 8, serverpath.indexOf(':' + _port));
		console.log(_path)
		console.log(_host)

		var req = https.request({
			hostname: _host,
			port: _port,
			path: _path
		}, function (res) {
			var _len = res.headers['content-length'];
			if (_len == null) {
				console.log("can not download because the app is no longer exist");

				if (callback) callback.apply([], this);
				return;
			}
			var totalLength = Number(_len);

			var currentLength = 0;
			res.on('data', function (data) {
				currentLength += data.length;
				file.write(data);
				//console.log("Downloading " + localpath.substring(localpath.lastIndexOf('/')+1) +" Version: "+version +" ... " +  ((currentLength/totalLength)*100+"").substring(0,4) +"%");
			});
			res.on('end', function () {
				file.end();
				if (localpath.indexOf('apk') > 0 || localpath.indexOf('ipa') > 0) {
					console.log("Download succeed!");
					var storeFile = localpath.substring(localpath.lastIndexOf('\\') + 1);
					fs.exists(storeFile, function (exists) {
						if (exists) {
							fs.unlinkSync(storeFile);
						}
						copyFile(localpath, storeFile);
					});
				}
				if (callback) callback.apply([], this);
			});
		});
		req.on('error', function (e) {
			console.log('problem with download ' + serverpath + ' : ' + e.message);
			console.log(e)
			try {
				fs.rmdirSync(folder);
			} catch (e) {
				console.log("can not download");
			}
			if (callback) callback.apply([], this);
		});
		// write data to request body
		if (localpath.indexOf('apk') < 0) {
			req.write('data\n');
			req.write('data\n');
		}
		req.end();
	};
	fs.exists(folder, function (exists) {
		if (exists) {
			startDownload();
		} else {
			var mkdir = 'mkdir ' + folder;
			exec(mkdir, function (err, stdout, stderr) {
				if (err) {
					console.log("can not create folder ");
					if (callback) callback.apply([], this);
				} else {
					startDownload();
				}
			});
		}
	});
};
var parseAndDownloadIpa = function (buildNo, callback) {
	var req = https.request({
		hostname: "xxxx",
		port: 8443,
		path: "/job/anw.ios-poc2-CI-darwinintel64_dev-darwinintel64_dev/lastSuccessfulBuild/artifact/gen/out/artifactsRedirect/artifacts/xx/anwstream/anwstream-Release.ipa.htm",
		method: "GET",
	}, function (res) {
		var buffer = "";
		res.setEncoding("utf-8");
		res.on('data', function (data) {
			buffer += data;
		});
		res.on('end', function () {
			if (buffer.length > 0) {
				var start = buffer.indexOf("URL=");
				var end = buffer.indexOf("Release.ipa");
				if (start > 0 && end > 0 && end > start) {
					var ipaPath = buffer.substring(start + 4, end + 11);
					console.log("new ipa path:" + ipaPath);
					downloadFile(ipaPath, 'ios/' + buildNo + "/anwstream.ipa", callback, "8081");
				}
			}
		});
	});
	// write data to request body
	req.write('data\n');
	req.write('data\n');
	req.end();
};
var checkIOSBuild = function (callback) {
	var buffer = "";
	var req = https.request({
		hostname: "xxx",
		port: 8443,
		path: "/job/anw.ios-poc2-CI-darwinintel64_dev-darwinintel64_dev/lastSuccessfulBuild/buildNumber",
		method: "GET",
	}, function (res) {
		res.setEncoding('utf8');
		res.on('data', function (data) {
			buffer += data;
		});
		res.on('end', function () {
			var buildNo = buffer;
			if (!isNaN(buildNo)) {
				console.log("Latest iOS version :" + buildNo + 'ios/' + buildNo + "/anwstream.ipa");
				fs.exists('ios/' + buildNo + "/anwstream.ipa", function (exists) {
					if (!exists) {
						parseAndDownloadIpa(buildNo, callback);
					} else {
						console.log(new Date() + "no update for iOS");
						if (callback) callback.apply([], this);
					}
				});
			}
		});
	});
	req.on('error', function (e) {
		if (callback) callback.apply([], this);
	});
	// write data to request body
	req.write('data\n');
	req.write('data\n');
	req.end();
};
var checkAndroidBuild = function (callback) {

	var buffer = "";
	var fail = false;
	var req = https.request({
		hostname: "xxxx",
		port: 8443,
		path: "/job/android-stream-develop-CI-docker_rhel/lastSuccessfulBuild/buildNumber",
		method: "GET",
		ca: "xx.crt"
	}, function (res) {
		res.setEncoding('utf8');
		res.on('data', function (data) {
			buffer += data;
		});
		res.on('end', function () {
			if (fail) {
				return;
			}
			var buildNo = buffer;
			if (!isNaN(buildNo)) {
				console.log("Latest android version :" + buildNo);
				fs.exists('android\\' + buildNo + "\\streamAndroid.apk", function (exists) {
					if (!exists) {
						var EventEmitter = require("events").EventEmitter;
						var body = new EventEmitter();
						var options = {
							hostname: 'xxxxxx',
							port: 8443,
							path: '/job/android-stream-develop-CI-docker_rhel/lastSuccessfulBuild/artifact/gen/deploymentInfo.log',
							method: 'GET'
						};

						var req = https.request(options, function (res) {
							res.on('data', function (d) {
								body.url = JSON.parse(d).deploymentInfos[0].URL;
								body.emit('update');
							});

						});

						//end the request
						req.end();
						req.on('error', function (err) {
							console.log("Error: ", err);
						});

						body.on('update', function () {
							console.log(body.url); // HOORAY! THIS WORKS!
							downloadFile(body.url, 'android\\' + buildNo + "\\streamAndroid.apk", callback, "8081");
						});


					} else {
						console.log(new Date() + "no update for Android");
						if (callback) callback.apply([], this);
					}
				});
			}
		});
	});
	req.on('error', function (e) {
		fail = true;
		console.log(e);
		if (callback) callback.apply([], this);
	});
	// write data to request body
	//req.write('data\n');
	//req.write('data\n');
	req.end();
};

checkIOSBuild(function () {
	setTimeout(function () {
		checkAndroidBuild(function () {
			console.log("all done.");
		});
	}, 3500);

});

setInterval(function () {
	checkIOSBuild(function () {
		setTimeout(function () {
			checkAndroidBuild(function () {
				console.log("all done.");
			});
		}, 3500);
	});
}, 1000 * 60 * 6);
  
}());