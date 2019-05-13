import click
import pynetbox
import unomaly


@click.command()
@click.option("--netbox-api-url", help="URL to netbox API", required=True)
@click.option("--netbox-api-token", help="Netbox API token", required=True)
@click.option("--unomaly-api-url", help="Unomaly API token", required=True)
@click.option("--unomaly-api-token", help="Unomaly API token", required=True)
@click.option("--noop", help="No-op execution", default=False, is_flag=True)
def run(
        netbox_api_url,
        netbox_api_token,
        unomaly_api_url,
        unomaly_api_token,
        noop
        ):
    nb = pynetbox.api(
      netbox_api_url,
      token=netbox_api_token
    )

    u = unomaly.api(
        unomaly_api_url,
        token=unomaly_api_token,
        ssl_verify=False
    )

    # Unomaly top level groups maps to a Netbox rack group,
    # subsequently the subgroups in Unomaly map to a specific rack.
    unomaly_groups = []
    unomaly_subgroups = []
    for g in u.get_all_groups():
        if g.has_parent():
            unomaly_subgroups.append((g.name, g.id))
        unomaly_groups.append((g.name, g.id))

    # unomaly_groups_by_id = dict((val, key) for (key, val) in unomaly_groups)
    unomaly_groups_by_name = dict(unomaly_groups)
    # unomaly_subgroups_by_id = dict((val, key) for (key, val) in unomaly_subgroups)
    unomaly_subgroups_by_name = dict(unomaly_subgroups)

    unomaly_groups = {
        **unomaly_groups_by_name,
        **unomaly_subgroups_by_name
    }

    # Creates a rack_group->rack mapping, creates groups as needed
    for rg in nb.dcim.rack_groups.all():
        if not unomaly_groups_by_name.get(rg.name):
            if not noop:
                gid = u.create_group(rg.name)
                click.echo(f"Created Unomaly group {rg.name} with id {gid}")
        else:
            gid = unomaly_groups_by_name.get(rg.name)
        for rack in nb.dcim.racks.filter(group_id=rg.id):
            if not unomaly_subgroups_by_name.get(rack.name):
                if not noop:
                    click.echo(f"Creating Unomaly group {rack.name}, subgroup"
                               f" of {rg.name}")
                    u.create_group(rack.name, parent_id=gid)

    # Time to assign systems!
    # Step 1) Find devices in Netbox based on fields from Unomaly
    for system in u.get_all_systems():
        device = nb.dcim.devices.get(name=system.name)
        if device:
            click.echo(f"Found device {device.name}")
            system_groups = []
            current_groups = system.groups
            if current_groups:
                system_groups = [group['name'] for group in current_groups]
            if device.rack not in system_groups:
                # Add to Unomaly group here.
                if not noop:
                    system.add_to_group(unomaly_groups.get(device.rack.name))
                    click.echo(f"Adding {system.name} to "
                               f"{unomaly_groups.get(device.rack.name)}")
        else:
            pass
            # click.echo(f"Couldn't find device via name {system.name} in Netbox")


if __name__ == '__main__':
    run()
