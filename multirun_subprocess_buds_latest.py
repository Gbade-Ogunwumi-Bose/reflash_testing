import subprocess
import time
import os


class MultiRunSubProcess(object):

    def __init__(self):
        print("__init__")

    def execute_command(self, cmd):
        conan_cmd = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        # print(cmd)
        try:
            output, errors = conan_cmd.communicate()  # timeout = 300 sec
            ret_code = conan_cmd.returncode
            print("sub process return code = {}".format(ret_code))
            print("sub process error = {}".format(errors))
            print("sub process output = {}".format(output.decode("utf-8")))
        except subprocess.TimeoutExpired as e:
            # print("timeout exception during execution of subprocess")
            conan_cmd.kill()
            ret_code = -1
            output = ""

        if ret_code != 0:
            return False, errors
        else:
            return True, str(output.decode("utf-8"))


if __name__ == '__main__':

    obj = MultiRunSubProcess()
    fw_ping_path = "C:\\Project\\Smalls\MBoards\\Encrypted\\0.11.6\\QCC517X_dfu_file.bin"
    fw_base_path = "C:\\Project\\Smalls\MBoards\\Encrypted\\0.10.26\\QCC517X_dfu_file.bin"
    case_fw_base_path = "C:\\Project\\Smalls\Case\\0.10.16\\SmallsCase.bin.dfu"
    case_fw_ping_path = "C:\\Project\\Smalls\Case\\0.10.17\\SmallsCase.bin.dfu"
    fw_ver_ping = "0.11.6"
    fw_ver_base = "0.10.26"
    case_serial = "M20920110028742590100C0"  # "M20920043018742590100C0"
    right_bud_mac = "C8:7B:23:51:BD:4A"  # "C8:7B:23:51:C7:B4"
    # "C8:7B:23:51:C5:B0"  # "78:2B:64:7C:3D:C2"  # "78:2B:64:7C:44:B1"
    left_bud_mac = "C8:7B:23:51:C0:03"  # "C8:7B:23:51:C4:80"
    # "C8:7B:23:51:BF:9A"    # "78:2B:64:7C:3D:D5"  # "78:2B:64:7C:45:26"
    echo_1_r = "echo \"right version before update started\""
    echo_2_r = "echo \"right version after update finished\""
    echo_1_l = "echo \"left version before update started\""
    echo_2_l = "echo \"left version after update finished\""
    connect_right_bud = "BoseManufacturingTool.exe ble_connect --ble_address {}".format(right_bud_mac)
    connect_left_bud = "BoseManufacturingTool.exe ble_connect --ble_address {}".format(left_bud_mac)

    disconnect_left_bud = "BoseManufacturingTool.exe ble_disconnect --ble_address {}".format(left_bud_mac)

    charging_disable_right = "BoseManufacturingTool.exe send \"Manufacturing.ChargerEnabled.SetGet 0\" " \
                             "--transport BLE --protocol BMAP --ble_insecure " \
                             "--expect \"Manufacturing.ChargerEnabled.Status .*\" " \
                             "--print_response --ble_address {}".format(right_bud_mac)

    charging_disable_left = "BoseManufacturingTool.exe send \"Manufacturing.ChargerEnabled.SetGet 0\" " \
                            "--transport BLE --protocol BMAP --ble_insecure " \
                            "--expect \"Manufacturing.ChargerEnabled.Status .*\" " \
                            "--print_response --ble_address {}".format(left_bud_mac)

    bat_sum_right = "BoseManufacturingTool.exe send \"BatteryDebug.Summary.Get\" " \
                    "--transport BLE --protocol BMAP --ble_insecure " \
                    "--expect \"BatteryDebug.Summary.Status .*\" --print_response " \
                    "--ble_address {}".format(right_bud_mac)
    bat_sum_left = "BoseManufacturingTool.exe send \"BatteryDebug.Summary.Get\" " \
                   "--transport BLE --protocol BMAP --ble_insecure " \
                   "--expect \"BatteryDebug.Summary.Status .*\" --print_response --ble_address {}".format(left_bud_mac)

    base_to_ping_update = "BoseManufacturingTool.exe update {} --ble_insecure --use_new_spitfire_init " \
                          "--peripheral_update_timeout 1800".format(fw_ping_path)
    ping_to_base_update = "BoseManufacturingTool.exe update {} --ble_insecure --use_new_spitfire_init " \
                          "--peripheral_update_timeout 1800".format(fw_base_path)

    case_base_to_ping_update = "BoseManufacturingTool.exe update {} " \
                               "--transport USB --serial_number \"{}\"".format(case_fw_ping_path, case_serial)
    case_ping_to_base_update = "BoseManufacturingTool.exe update {} " \
                               "--transport USB --serial_number \"{}\"".format(case_fw_base_path, case_serial)
    version_cmd_right = "BoseManufacturingTool.exe send \"ProductInfo.FirmwareVersion.Get\" " \
                        "--transport BLE --protocol BMAP --ble_insecure " \
                        "--expect \"ProductInfo.FirmwareVersion.Status .*\" " \
                        "--print_response --ble_address {}".format(right_bud_mac)
    version_cmd_left = "BoseManufacturingTool.exe send \"ProductInfo.FirmwareVersion.Get\" " \
                       "--transport BLE --protocol BMAP --ble_insecure " \
                       "--expect \"ProductInfo.FirmwareVersion.Status .*\" " \
                       "--print_response --ble_address {}".format(left_bud_mac)

    anr_version_cmd_right = "BoseManufacturingTool.exe send \"SmartANRPlatform.FirmwareVersion.Get\" " \
                            "--transport BLE --protocol BMAP --ble_insecure " \
                            "--expect \"SmartANRPlatform.FirmwareVersion.Status .*\" " \
                            "--print_response --ble_address {}".format(right_bud_mac)
    anr_version_cmd_left = "BoseManufacturingTool.exe send \"SmartANRPlatform.FirmwareVersion.Get\" " \
                           "--transport BLE --protocol BMAP --ble_insecure " \
                           "--expect \"SmartANRPlatform.FirmwareVersion.Status .*\" " \
                           "--print_response --ble_address {}".format(left_bud_mac)

    sensor_info_cmd_right = "BoseManufacturingTool.exe send \"SensorInterface.SensorInfo.Get 4,1,0\" " \
                            "--transport BLE --protocol BMAP --ble_insecure " \
                            "--expect \"SensorInterface.SensorInfo.Status .*\" " \
                            "--print_response --ble_address {}".format(right_bud_mac)
    sensor_info_cmd_left = "BoseManufacturingTool.exe send \"SensorInterface.SensorInfo.Get 4,0,0\" " \
                           "--transport BLE --protocol BMAP --ble_insecure " \
                           "--expect \"SensorInterface.SensorInfo.Status .*\" " \
                           "--print_response --ble_address {}".format(left_bud_mac)

    case_version_cmd = "BoseManufacturingTool.exe send \"ProductInfo.FirmwareVersion.Get\" " \
                       "--protocol BMAP --transport USB --serial_number \"{}\" " \
                       "--expect \"ProductInfo.FirmwareVersion.Status .*\" --print_response".format(case_serial)

    charging_disable_Case = "BoseManufacturingTool.exe send \"Manufacturing.ChargerEnabled.SetGet 0\" " \
                            "--transport USB --protocol BMAP --serial_number \"{}\" " \
                            "--expect \"Manufacturing.ChargerEnabled.Status .*\" " \
                            "--print_response".format(case_serial)
    bat_sum_Case = "BoseManufacturingTool.exe send \"BatteryDebug.Summary.Get\" " \
                   "--transport USB --protocol BMAP --serial_number \"{}\" " \
                   "--expect \"BatteryDebug.Summary.Status .*\" --print_response".format(case_serial)

    dongle_reset = "BoseManufacturingTool.exe dongle_reset"

    factory_reset_right_bud = "BoseManufacturingTool.exe send \"Control.FactoryDefault.Start\" " \
                              "--transport BLE --protocol BMAP --ble_insecure " \
                              "--expect \"Control.FactoryDefault.Processing *\" " \
                              "--print_response --ble_address {}".format(right_bud_mac)

    mfg_earbud_add_get_right_bud = "BoseManufacturingTool.exe send \"Manufacturing.EarbudAddress.Get\" " \
                                   "--transport BLE --protocol BMAP --ble_insecure " \
                                   "--expect \"Manufacturing.EarbudAddress.Status .*\" " \
                                   "--print_response --ble_address {}".format(right_bud_mac)
    mfg_earbud_add_get_left_bud = "BoseManufacturingTool.exe send \"Manufacturing.EarbudAddress.Get\" " \
                                  "--transport BLE --protocol BMAP --ble_insecure " \
                                  "--expect \"Manufacturing.EarbudAddress.Status .*\" " \
                                  "--print_response --ble_address {}".format(left_bud_mac)

    mfg_earbud_pair_get_right_bud = "BoseManufacturingTool.exe send \"Manufacturing.EarbudPair.Get\" " \
                                    "--transport BLE --protocol BMAP --ble_insecure " \
                                    "--expect \"Manufacturing.EarbudPair.Status .*\" " \
                                    "--print_response --ble_address {}".format(right_bud_mac)
    mfg_earbud_pair_get_left_bud = "BoseManufacturingTool.exe send \"Manufacturing.EarbudPair.Get\" " \
                                   "--transport BLE --protocol BMAP --ble_insecure " \
                                   "--expect \"Manufacturing.EarbudPair.Status .*\" " \
                                   "--print_response --ble_address {}".format(left_bud_mac)
    bat_timestamp_right = "BoseManufacturingTool.exe send \"BatteryDebug.VoltageTimeStamp.Get\" " \
                          "--transport BLE --protocol BMAP --ble_insecure " \
                          "--expect \"BatteryDebug.VoltageTimeStamp.Status .*\" " \
                          "--print_response --ble_address {}".format(right_bud_mac)
    bat_timestamp_left = "BoseManufacturingTool.exe send \"BatteryDebug.VoltageTimeStamp.Get\" " \
                         "--transport BLE --protocol BMAP --ble_insecure " \
                         "--expect \"BatteryDebug.VoltageTimeStamp.Status .*\" " \
                         "--print_response --ble_address {}".format(left_bud_mac)

    case_reset = "BoseManufacturingTool.exe send \"Control.Reset.Start\" " \
                 "--protocol BMAP --transport USB --serial_number \"{}\" " \
                 "--expect \"Control.Reset.Result .*\" --print_response".format(case_serial)

    psm_btn_1_right = "BoseManufacturingTool.exe send \"Debug.TAP.Start \"psm.disp btn,1\"\" --transport BLE " \
                      "--protocol BMAP --ble_insecure --expect \" * \" --print_response " \
                      "--ble_address {}".format(right_bud_mac)
    psm_btn_1_left = "BoseManufacturingTool.exe send \"Debug.TAP.Start \"psm.disp btn,1\"\" --transport BLE " \
                     "--protocol BMAP --ble_insecure --expect \" * \" --print_response " \
                     "--ble_address {}".format(left_bud_mac)

    result_lst = []


    def update_seq(log_file, update_cmd, case_update_cmd):

        # reset the dongle
        _, _ = obj.execute_command("echo \"--------------dongle_reset------------------\"" + log_file)
        _, _ = obj.execute_command(dongle_reset + log_file)
        # wait for dongle to come back in the proper state.
        time.sleep(2)
        _, _ = obj.execute_command("echo \"--------------case_reset------------------\"" + log_file)
        _, _ = obj.execute_command(case_reset + log_file)
        time.sleep(5)

        # disable case charging after case reset
        _, _ = obj.execute_command("echo \"--------------case_charging_disable------------------\"" + log_file)
        _, _ = obj.execute_command(charging_disable_Case + log_file)
        _, _ = obj.execute_command("echo \"-----Case version initially--------\"" + log_file)
        _, _ = obj.execute_command(case_version_cmd + log_file)
        _, _ = obj.execute_command("echo \"--------------case_sum------------------\"" + log_file)
        _, _ = obj.execute_command(bat_sum_Case + log_file)

        # connect to right buds and disable charging
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        _, _ = obj.execute_command(connect_right_bud + log_file)
        # _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        # _, _ = obj.execute_command(connect_left_bud + log_file)
        # _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        # _, _ = obj.execute_command("echo \"charging_disable_right\"" + log_file)
        # _, _ = obj.execute_command(charging_disable_right + log_file)
        # _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        # _, _ = obj.execute_command("echo \"charging_disable_left\"" + log_file)
        # _, _ = obj.execute_command(charging_disable_left + log_file)
        # _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)

        # factory default to right bud without payload(it will FD to both the buds)
        _, _ = obj.execute_command("echo \"-------------factory_reset_right_bud-------------------\"" + log_file)
        _, _ = obj.execute_command(factory_reset_right_bud + log_file)

        # wait for buds to comeback or reboot
        time.sleep(15)

        # 1. connect to both the buds
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        _, _ = obj.execute_command(connect_right_bud + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        _, _ = obj.execute_command(connect_left_bud + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        # 3. execute disable charging and battery summery command
        _, _ = obj.execute_command("echo \"charging_disable_right\"" + log_file)
        _, _ = obj.execute_command(charging_disable_right + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        _, _ = obj.execute_command("echo \"charging_disable_left\"" + log_file)
        _, _ = obj.execute_command(charging_disable_left + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        # time.sleep(1)
        #
        # _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        # _, _ = obj.execute_command(connect_right_bud + log_file)
        # _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        # _, _ = obj.execute_command(connect_left_bud + log_file)
        # _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)

        _, _ = obj.execute_command("echo \"bat_sum_right\"" + log_file)
        _, _ = obj.execute_command(bat_sum_right + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        _, _ = obj.execute_command("echo \"bat_sum_left\"" + log_file)
        _, _ = obj.execute_command(bat_sum_left + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        _, _ = obj.execute_command("echo \"--------------case_bat_sum------------------\"" + log_file)
        _, _ = obj.execute_command(bat_sum_Case + log_file)

        # check peer pairing of buds and get the peer mac address using MFG commands
        _, _ = obj.execute_command("echo \"-----------right bud peer mac address---------------------\"" + log_file)
        _, _ = obj.execute_command(mfg_earbud_add_get_right_bud + log_file)
        _, _ = obj.execute_command("echo \"-----------left bud peer mac address---------------------\"" + log_file)
        _, _ = obj.execute_command(mfg_earbud_add_get_left_bud + log_file)
        _, _ = obj.execute_command("echo \"-----------right bud peer pairing---------------------\"" + log_file)
        _, _ = obj.execute_command(mfg_earbud_pair_get_right_bud + log_file)
        _, _ = obj.execute_command("echo \"-----------left bud peer pairing---------------------\"" + log_file)
        _, _ = obj.execute_command(mfg_earbud_pair_get_left_bud + log_file)

        # 2. get before version of both the buds
        _, _ = obj.execute_command(echo_1_r + log_file)
        _, _ = obj.execute_command(version_cmd_right + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        _, _ = obj.execute_command(echo_1_l + log_file)
        _, _ = obj.execute_command(version_cmd_left + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)

        _, _ = obj.execute_command("echo \"-----Right bud smart ANR ver before update--------------\"" + log_file)
        _, _ = obj.execute_command(anr_version_cmd_right + log_file)
        _, _ = obj.execute_command("echo \"-----Left bud smart ANR ver before update--------------\"" + log_file)
        _, _ = obj.execute_command(anr_version_cmd_left + log_file)

        _, _ = obj.execute_command("echo \"-----Right bud sensor ver before update--------------\"" + log_file)
        _, _ = obj.execute_command(sensor_info_cmd_right + log_file)
        _, _ = obj.execute_command("echo \"-----Left bud sensor ver before update--------------\"" + log_file)
        _, _ = obj.execute_command(sensor_info_cmd_left + log_file)

        # 4. update to base->ping
        # 4.5 disconnect left bud as BLE update needs ony 1 dut connection --ble_address argument is not working
        _, _ = obj.execute_command(disconnect_left_bud + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        # res, output = obj.execute_command(update_cmd + log_file)
        res = False
        output = "Got here"
        if not res:
            return res, False, output

        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        # 5. get after version of both the buds
        _, _ = obj.execute_command(connect_left_bud + log_file)
        _, _ = obj.execute_command("echo \"charging_disable_right\"" + log_file)
        _, _ = obj.execute_command(charging_disable_right + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        _, _ = obj.execute_command("echo \"charging_disable_left\"" + log_file)
        _, _ = obj.execute_command(charging_disable_left + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)

        # if update failed then get update.state and earbud.state, also run a loop of 5-10 with update.sync
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        _, _ = obj.execute_command(echo_2_r + log_file)
        _, _ = obj.execute_command(version_cmd_right + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        _, _ = obj.execute_command(echo_2_l + log_file)
        _, _ = obj.execute_command(version_cmd_left + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        _, _ = obj.execute_command("echo \"-----Right bud smart ANR ver after update--------------\"" + log_file)
        _, _ = obj.execute_command(anr_version_cmd_right + log_file)
        _, _ = obj.execute_command("echo \"-----Left bud smart ANR ver after update--------------\"" + log_file)
        _, _ = obj.execute_command(anr_version_cmd_left + log_file)

        _, _ = obj.execute_command("echo \"-----Right bud sensor ver after update--------------\"" + log_file)
        _, _ = obj.execute_command(sensor_info_cmd_right + log_file)
        _, _ = obj.execute_command("echo \"-----Left bud sensor ver after update--------------\"" + log_file)
        _, _ = obj.execute_command(sensor_info_cmd_left + log_file)

        # Case Update
        _, _ = obj.execute_command("echo \"-----Case version before--------\"" + log_file)
        _, _ = obj.execute_command(case_version_cmd + log_file)
        _, _ = obj.execute_command("echo \"-----Case update--------\"" + log_file)
        res_case, _ = obj.execute_command(case_update_cmd + log_file)
        if not res_case:
            return res, res_case

        # wait for buds and Case to comeback after reboot
        time.sleep(5)

        _, _ = obj.execute_command("echo \"--------------case_charging_disable------------------\"" + log_file)
        _, _ = obj.execute_command(charging_disable_Case + log_file)
        _, _ = obj.execute_command("echo \"-----Case version after--------\"" + log_file)
        _, _ = obj.execute_command(case_version_cmd + log_file)
        _, _ = obj.execute_command("echo \"--------------case_sum after update------------------\"" + log_file)
        _, _ = obj.execute_command(bat_sum_Case + log_file)
        time.sleep(5)
        _, _ = obj.execute_command("echo \"-----connecting right bud--------\"" + log_file)
        _, _ = obj.execute_command(connect_right_bud + log_file)
        _, _ = obj.execute_command("echo \"-----connecting left bud--------\"" + log_file)
        _, _ = obj.execute_command(connect_left_bud + log_file)
        _, _ = obj.execute_command(echo_2_r + log_file)
        _, _ = obj.execute_command(version_cmd_right + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        _, _ = obj.execute_command(echo_2_l + log_file)
        _, _ = obj.execute_command(version_cmd_left + log_file)
        _, _ = obj.execute_command("echo \"bat_sum_right after update\"" + log_file)
        _, _ = obj.execute_command(bat_sum_right + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        _, _ = obj.execute_command("echo \"bat_sum_left after update\"" + log_file)
        _, _ = obj.execute_command(bat_sum_left + log_file)
        _, _ = obj.execute_command("echo \"--------------------------------\"" + log_file)
        _, _ = obj.execute_command("echo \"--------------case_bat_sum------------------\"" + log_file)
        _, _ = obj.execute_command(bat_sum_Case + log_file)

        return res, res_case


    for x in range(1):
        print("running loop index is {}".format(x))
        cmd1_logfile = " >> BMT_Test_logs\\C2_16\\{}_log_updating_to_{}.txt 2>&1".format(x, fw_ver_ping)
        cmd2_logfile = " >> BMT_Test_logs\\C2_16\\{}_log_updating_to_{}.txt 2>&1".format(x, fw_ver_base)
        print("#####################base_to_ping_update############################## loop index is {}".format(x))

        # base to ping update
        for attempt in range(2):
            try:
                res1, case_res1, _ = update_seq(cmd1_logfile, base_to_ping_update, case_base_to_ping_update)
                if not res1:
                    # raise exception if update cmd fails
                    raise ValueError(f"Update command failed from previous execution: {_}")
            except ValueError:
                # overwrite logfile name, so retry is in a separate file
                cmd1_logfile = f" >> BMT_Test_logs\\C2_16\\{x}_log_updating_to_{fw_ver_ping}_retry_{attempt+1}.txt 2>&1"
            else:
                # break out of re-attempt loop if all goes well
                break

        # ping to base update
        for attempt in range(2):
            try:
                res2, case_res2, _ = update_seq(cmd2_logfile, ping_to_base_update, case_ping_to_base_update)
                if not res2:
                    # raise exception if update cmd fails
                    raise ValueError(f"Update command failed from previous execution: {_}")
            except ValueError:
                # overwrite logfile name, so retry is in a separate file
                cmd2_logfile = f" >> BMT_Test_logs\\C2_16\\{x}_log_updating_to_{fw_ver_base}_retry_{attempt+1}.txt 2>&1"
            else:
                # break out of re-attempt loop if all goes well
                break

        result_lst.append(tuple((res1, res2)))
        result_lst.append((res1, res2))

    print("=============Results are==================")
    print(result_lst)
