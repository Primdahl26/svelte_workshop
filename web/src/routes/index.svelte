<script lang="ts">
	interface Insight {
		departmentName: string
		employeeEmail: string
		employeeName: string
		id: string
		managerEmail: string
		managersName: string
	}

	const defaultFields: string[] = [
		'id',
		'departmentName',
		'employeeEmail',
		'employeeName',
		'managerEmail',
		'managersName'
	]

	let selectedFields: string[] = defaultFields
	let skip = 0
	let limit = 10
	let insightQuery = `
      query MyQuery {
        getInsight(skip: ${skip}, limit: ${limit}) {
          id
          departmentName
          employeeEmail
          employeeName
          managerEmail
          managersName
        }
      }
    `
	const buildQuery = (skip: number = 0, limit: number = 10, fields: string[] = defaultFields) => {
		return `
      query MyQuery {
        getInsight(skip: ${skip}, limit: ${limit}) {
          ${fields.join(' ')}
        }
      }
    `
	}

	// The callback way
	// const fetchInsight: Promise<Insight[]> = fetch('http://localhost:2000/graphql', {
	// 	method: 'POST',
	// 	headers: {
	// 		'Content-Type': 'application/json'
	// 	},
	// 	body: JSON.stringify({
	// 		query: insightQuery
	// 	})
	// })
	// 	.then((res) => res.json())
	// 	.then((result) => {
	// 		console.log('lol')
	// 		return result.data.getInsight
	// 	})

	// The "oldschool" way
	const fetchInsight = async (): Promise<Insight[]> => {
		const res = await fetch('http://localhost:2000/graphql', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				query: insightQuery
			})
		})

		const result = await res.json()
		return result.data.getInsight
	}

	let data: Promise<Insight[]> | Insight[] = fetchInsight()

	const refresh = () => {
		data = fetchInsight()
	}

	// Holds table sort state.  Initialized to reflect table sorted by id column ascending.
	let sortBy = { col: 'id', ascending: true }

	$: sort = async (column: string) => {
		if (sortBy.col == column) {
			sortBy.ascending = !sortBy.ascending
		} else {
			sortBy.col = column
			sortBy.ascending = true
		}

		// Modifier to sorting function for ascending or descending
		let sortModifier = sortBy.ascending ? 1 : -1

		let sort = (a: any, b: any) =>
			a[column] < b[column] ? -1 * sortModifier : a[column] > b[column] ? 1 * sortModifier : 0

		data = (await data).sort(sort)
	}

	$: {
		if (limit) {
			insightQuery = buildQuery(skip, limit, selectedFields)
			refresh()
		}
	}
</script>

<h1>Velkommen til indsigt</h1>

<label for="skip">Skip</label>
<input name="skip" type="number" min="0" bind:value={skip} />
<label for="limit">Limit</label>
<input name="limit" type="number" min="0" max="1000" bind:value={limit} />
<label for="fields">Fields</label>

{#each defaultFields as field}
	<input
		name={field}
		type="checkbox"
		on:change={() => {
			if (selectedFields.includes(field)) {
				selectedFields = selectedFields.filter((e) => e !== field)
			} else {
				selectedFields.push(field)
			}
			insightQuery = buildQuery(skip, limit, selectedFields)
			refresh()
		}}
		checked
	/>
	{field}
	<br />
{/each}

<br />
<table>
	<thead>
		<tr>
			{#each selectedFields as header}
				<th scope="col" on:click={() => sort(header)}>{header}</th>
			{/each}
		</tr>
	</thead>
	{#await data}
		<tbody>
			<tr>
				{#each selectedFields as _}
					<th aria-busy="true" />
				{/each}
			</tr>
		</tbody>
	{:then insights}
		{#each insights as insight}
			<tbody>
				<tr>
					{#each Object.values(insight) as field}
						<td>{field}</td>
					{/each}
				</tr>
			</tbody>
		{/each}
	{/await}
</table>
