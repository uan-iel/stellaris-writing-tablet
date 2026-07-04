use std::{
    env, fs,
    path::{Path, PathBuf},
};

#[tauri::command]
fn save_app_snapshot(contents: String) -> Result<String, String> {
    let directory = durable_data_dir()
        .unwrap_or_else(|| env::current_dir().unwrap_or_else(|_| PathBuf::from(".")));

    fs::create_dir_all(&directory)
        .map_err(|error| format!("Could not create data folder: {error}"))?;

    let path = directory.join("stellaris-data.json");
    let temporary_path = directory.join("stellaris-data.tmp");

    fs::write(&temporary_path, contents)
        .map_err(|error| format!("Could not write temporary data file: {error}"))?;
    fs::rename(&temporary_path, &path)
        .map_err(|error| format!("Could not replace data file: {error}"))?;

    Ok(path.display().to_string())
}

#[tauri::command]
fn load_app_snapshot() -> Result<Option<String>, String> {
    let Some(directory) = durable_data_dir() else {
        return Ok(None);
    };
    let path = directory.join("stellaris-data.json");

    if !path.exists() {
        return Ok(None);
    }

    fs::read_to_string(&path)
        .map(Some)
        .map_err(|error| format!("Could not read data file: {error}"))
}

#[tauri::command]
fn export_migration_file(contents: String) -> Result<String, String> {
    let mut directory = downloads_dir()
        .unwrap_or_else(|| env::current_dir().unwrap_or_else(|_| PathBuf::from(".")));
    directory.push("Stellaris Migrations");

    fs::create_dir_all(&directory)
        .map_err(|error| format!("Could not create migration folder: {error}"))?;

    let timestamp = unix_timestamp();
    let filename = format!("stellaris-migration-{timestamp}.json");
    let path = unique_file_path(&directory, &filename);

    fs::write(&path, contents)
        .map_err(|error| format!("Could not export migration file: {error}"))?;

    Ok(path.display().to_string())
}

fn downloads_dir() -> Option<PathBuf> {
    env::var_os("HOME").map(|home| PathBuf::from(home).join("Downloads"))
}

fn durable_data_dir() -> Option<PathBuf> {
    documents_dir().map(|directory| directory.join("Stellaris Writing"))
}

fn documents_dir() -> Option<PathBuf> {
    if cfg!(target_os = "windows") {
        env::var_os("USERPROFILE").map(|home| PathBuf::from(home).join("Documents"))
    } else {
        env::var_os("HOME").map(|home| PathBuf::from(home).join("Documents"))
    }
}

fn unix_timestamp() -> u64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|duration| duration.as_secs())
        .unwrap_or(0)
}

fn unique_file_path(directory: &Path, filename: &str) -> PathBuf {
    let original = Path::new(filename);
    let stem = original
        .file_stem()
        .and_then(|value| value.to_str())
        .unwrap_or("Untitled Note");
    let extension = original
        .extension()
        .and_then(|value| value.to_str())
        .unwrap_or("md");
    let mut path = directory.join(filename);
    let mut index = 2;

    while path.exists() {
        path = directory.join(format!("{stem} ({index}).{extension}"));
        index += 1;
    }

    path
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_clipboard_manager::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_os::init())
        .setup(|app| {
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;
            }
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            save_app_snapshot,
            load_app_snapshot,
            export_migration_file
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
