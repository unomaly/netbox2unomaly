import click
import pynetbox

# In [34]: dict(o)
# Out[34]:
# {'id': 1,
#  'name': 'leaf-sw-001',
#  'display_name': 'leaf-sw-001',
#  'device_type': {'id': 1,
#   'url': 'http://localhost:32768/api/dcim/device-types/1/',
#   'manufacturer': {'id': 1,
#    'url': 'http://localhost:32768/api/dcim/manufacturers/1/',
#    'name': 'cisco',
#    'slug': 'cisco'},
#   'model': 'ASA-2345',
#   'slug': 'asa-2345',
#   'display_name': 'cisco ASA-2345'},
#  'device_role': {'id': 1,
#   'url': 'http://localhost:32768/api/dcim/device-roles/1/',
#   'name': 'leaf switch',
#   'slug': 'leaf-switch'},
#  'tenant': None,
#  'platform': None,
#  'serial': '',
#  'asset_tag': None,
#  'site': {'id': 1,
#   'url': 'http://localhost:32768/api/dcim/sites/1/',
#   'name': 'Stockholm DC1',
#   'slug': 'stockholm-dc1'},
#  'rack': {'id': 1,
#   'url': 'http://localhost:32768/api/dcim/racks/1/',
#   'name': 'rack 001',
#   'display_name': 'rack 001'},
#  'position': 36,
#  'face': {'value': 0, 'label': 'Front'},
#  'parent_device': None,
#  'status': {'value': 1, 'label': 'Active'},
#  'primary_ip': None,
#  'primary_ip4': None,
#  'primary_ip6': None,
#  'cluster': None,
#  'virtual_chassis': None,
#  'vc_position': None,
#  'vc_priority': None,
#  'comments': '',
#  'local_context_data': None,
#  'tags': [],
#  'custom_fields': {},
#  'config_context': {},
#  'created': '2019-03-04',
#  'last_updated': '2019-03-04T12:30:56.037395Z'}

# In [35]: dict(o.rack)
# Out[35]:
# {'id': 1,
#  'url': 'http://localhost:32768/api/dcim/racks/1/',
#  'name': 'rack 001',
#  'display_name': 'rack 001'}


@click.command()
@click.option("--netbox-api-url", help="URL to netbox API", required=True)
@click.option("--netbox-api-token", help="Netbox API token", required=True)
@click.option("--field-pattern", help="Netbox API token", required=True)
@click.option("--unomaly-api-url", help="Unomaly API token", required=True)
@click.option("--unomaly-api-token", help="Unomaly API token", required=True)
def run(netbox_api_url, netbox_api_token, unomaly_api_url, unomaly_api_token):
    # click.echo("Hello, %s" % netbox_api_url)
    # nb = pynetbox.api(
    #   netbox_api_url,
    #   token=netbox_api_token
    # )
    # click.echo(nb)
    # click.echo(nb.dcim.devices.all())


if __name__ == '__main__':
    run()
