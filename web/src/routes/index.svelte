<script lang="ts">
	interface Insight {
		departmentName: string
		employeeEmail: string
		employeeName: string
		id: string
		managerEmail: string
		managersName: string
	}

	let insightQuery = `
      query MyQuery {
        getInsight(skip: 0, limit: 5) {
          id
          departmentName
          employeeEmail
          employeeName
          managerEmail
          managersName
        }
      }
`
	const defaultFields: string[] = [
		'id',
		'departmentName',
		'employeeEmail',
		'employeeName',
		'managerEmail',
		'managersName'
	]

	let selectedFields: string[] = defaultFields

	const buildQuery = (skip: number = 0, limit: number = 5, fields: string[] = defaultFields) => {
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

	const modifyData = (event: Event) => {
		const element = event.target as HTMLFormElement
		const form = new FormData(element)

		selectedFields = []
		for (const x of form.entries()) {
			if (x[1] === 'on') {
				selectedFields.push(x[0])
			}
		}

		const skip: any = form.get('skip')
		const limit: any = form.get('limit')

		insightQuery = buildQuery(skip, limit, selectedFields)
		refresh()
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
</script>

<h1>Velkommen til indsigt</h1>

<form class="content" on:submit|preventDefault={modifyData}>
	<label for="skip">Skip</label>
	<input name="skip" type="number" value="0" />
	<label for="limit">Limit</label>
	<input name="limit" type="number" value="5" />
	<label for="fields">Fields</label>
	{#each defaultFields as field}
		<input name={field} type="checkbox" checked />
		{field}
		<br />
	{/each}
	<button type="submit">Submit</button>
</form>

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
